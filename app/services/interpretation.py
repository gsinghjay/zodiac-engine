"""Service for LLM-based astrological interpretation."""
import logging
from typing import Dict, Any, List, Optional

# Add new imports
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
import markdown

from app.schemas.report import NatalReportData, SynastryReportData, InterpretationResponse

logger = logging.getLogger(__name__)

class InterpretationService:
    """Service for generating astrological interpretations using LLM."""
    
    def __init__(self, llm_api_key: Optional[str] = None, model_name: str = "gpt-4", llm_provider: str = "openai"):
        """
        Initialize the InterpretationService.
        
        Args:
            llm_api_key: Optional API key for the LLM service
            model_name: Name of the model to use for interpretation
            llm_provider: Provider of the LLM service (openai, anthropic, gemini)
        """
        self.llm_api_key = llm_api_key
        self.model_name = model_name
        self.llm_provider = llm_provider
        self.model = None
        self.interpretation_prompts = {
            "natal": self._get_natal_prompt_template(),
            "synastry": self._get_synastry_prompt_template()
        }
        
        # Initialize Gemini if selected
        if self.llm_provider == "gemini":
            if self.llm_api_key:
                try:
                    genai.configure(api_key=self.llm_api_key)
                    self.model = genai.GenerativeModel(self.model_name)
                    logger.info(f"Gemini client initialized successfully with model: {self.model_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini client: {e}")
            else:
                logger.warning("Gemini provider selected, but LLM_API_KEY is missing.")
        else:
            logger.info(f"InterpretationService initialized for provider: {self.llm_provider} with model: {self.model_name}")
    
    def interpret_natal_chart(
        self,
        report_data: NatalReportData,
        aspects_focus: bool = True,
        houses_focus: bool = True,
        planets_focus: bool = True,
        tone: str = "neutral",
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an interpretation of a natal chart report.
        
        Args:
            report_data: Structured report data from the ReportService
            aspects_focus: Whether to focus on aspect interpretation
            houses_focus: Whether to focus on house placement interpretation
            planets_focus: Whether to focus on planet interpretation
            tone: Tone of the interpretation (neutral, detailed, beginner-friendly)
            max_length: Maximum length of the interpretation in words
            
        Returns:
            Dictionary containing the interpretation_html, highlights, and suggestions
        """
        logger.info("Generating natal chart interpretation")
        logger.debug(f"Interpretation parameters: aspects_focus={aspects_focus}, houses_focus={houses_focus}, planets_focus={planets_focus}, tone={tone}")
        
        # Prepare focus areas for prompt
        focus_areas = []
        if aspects_focus:
            focus_areas.append("Planetary aspects")
        if houses_focus:
            focus_areas.append("House placements")
        if planets_focus:
            focus_areas.append("Individual planet interpretations")
            
        focus_areas_text = ", ".join(focus_areas) if focus_areas else "all aspects of the chart"
        
        # Prepare the max length text for the prompt
        max_length_text = f"approximately {max_length} words in length" if max_length else "comprehensive but concise"
        
        # Log the report data we received
        logger.debug(f"Received report data with title: {report_data.title}")
        
        # Use Gemini if configured
        if self.llm_provider == "gemini" and self.model is not None:
            try:
                # Format the prompt with the report data
                prompt_text = self.interpretation_prompts["natal"].format(
                    title=report_data.title,
                    data_table=report_data.data_table,
                    planets_table=report_data.planets_table,
                    houses_table=report_data.houses_table,
                    full_report=report_data.full_report,
                    focus_areas=focus_areas_text,
                    tone=tone,
                    max_length_text=max_length_text
                )
                
                logger.debug("Sending prompt to Gemini API for natal interpretation")
                response = self.model.generate_content(prompt_text)
                
                if not response.text:
                    # Handle empty or blocked response
                    error_msg = "Gemini API returned empty content or blocked response"
                    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                        error_msg += f": {response.prompt_feedback.block_reason}"
                    logger.error(error_msg)
                    return {
                        "interpretation_html": f"<p>Unable to generate interpretation: {error_msg}</p>",
                        "highlights": ["Error occurred with Gemini API"],
                        "suggestions": ["Try adjusting your request or try again later"]
                    }
                
                # Get the markdown text from the response
                markdown_text = response.text
                
                # Convert Markdown to HTML
                interpretation_html = markdown.markdown(
                    markdown_text, 
                    extensions=['extra', 'nl2br', 'sane_lists']
                )
                
                logger.info("Successfully generated and converted interpretation with Gemini API")
                
                # Try to parse highlights and suggestions from markdown_text
                highlights = ["Generated by Gemini", "Based on astrological chart data"]
                suggestions = ["Explore specific planetary aspects", "Consider house positions for more insight"]
                
                try:
                    if "## Summary: Strengths & Challenges" in markdown_text:
                        strengths_section = markdown_text.split("## Summary: Strengths & Challenges")[1].split("##")[0]
                        if "Key Strengths:" in strengths_section:
                            strengths_text = strengths_section.split("Key Strengths:")[1].split("Potential Challenges:")[0]
                            strengths_list = [line.strip().lstrip('* ').lstrip('- ') 
                                            for line in strengths_text.splitlines() 
                                            if line.strip().startswith(('*', '-'))]
                            if strengths_list:
                                highlights = strengths_list
                    
                    if "## Practical Guidance & Suggestions" in markdown_text:
                        suggestions_section = markdown_text.split("## Practical Guidance & Suggestions")[1].split("##")[0]
                        suggestions_list = [line.strip().lstrip('* ').lstrip('- ') 
                                         for line in suggestions_section.splitlines() 
                                         if line.strip().startswith(('*', '-'))]
                        if suggestions_list:
                            suggestions = suggestions_list
                except Exception as e:
                    logger.warning(f"Could not parse highlights/suggestions from LLM output: {e}")
                
                return {
                    "interpretation_html": interpretation_html,
                    "highlights": highlights,
                    "suggestions": suggestions
                }
            
            except GoogleAPIError as e:
                logger.error(f"Gemini API error: {e}")
                return {
                    "interpretation_html": f"<p>Error calling Gemini API: {str(e)}</p>",
                    "highlights": ["API error occurred"],
                    "suggestions": ["Check API key and try again"]
                }
            except Exception as e:
                logger.exception(f"Unexpected error with Gemini API: {e}")
                return {
                    "interpretation_html": "<p>An unexpected error occurred while generating the interpretation.</p>",
                    "highlights": ["Error occurred"],
                    "suggestions": ["Please try again later"]
                }
        
        # Fallback for when Gemini is not configured
        logger.warning("Using placeholder response because Gemini is not configured or another provider is selected")
        return {
            "interpretation_html": f"<p>This is a placeholder interpretation for {report_data.title}. Please configure the LLM provider.</p>",
            "highlights": ["LLM not configured"],
            "suggestions": ["Configure LLM provider in settings"]
        }
    
    def interpret_synastry_chart(
        self,
        report_data: SynastryReportData,
        aspects_focus: bool = True,
        compatibility_focus: bool = True,
        tone: str = "neutral",
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an interpretation of a synastry chart report.
        
        Args:
            report_data: Structured report data containing both charts
            aspects_focus: Whether to focus on synastry aspect interpretation
            compatibility_focus: Whether to focus on overall compatibility
            tone: Tone of the interpretation (neutral, detailed, beginner-friendly)
            max_length: Maximum length of the interpretation in words
            
        Returns:
            Dictionary containing the interpretation_html, highlights, and suggestions
        """
        logger.info("Generating synastry chart interpretation")
        
        # Prepare focus areas for prompt
        focus_areas = []
        if aspects_focus:
            focus_areas.append("Planetary aspects between the charts")
        if compatibility_focus:
            focus_areas.append("Overall compatibility and relationship dynamics")
            
        focus_areas_text = ", ".join(focus_areas) if focus_areas else "all aspects of the relationship"
        
        # Prepare the max length text for the prompt
        max_length_text = f"approximately {max_length} words in length" if max_length else "comprehensive but concise"
        
        # Fallback for now
        # TODO: Implement synastry interpretation with Gemini similar to natal chart
        return {
            "interpretation_html": "<p>Synastry chart interpretation with markdown conversion will be implemented soon.</p>",
            "highlights": ["Implementation in progress"],
            "suggestions": ["Check back soon for synastry interpretation features"]
        }
        
    def _get_natal_prompt_template(self) -> str:
        """
        Get the prompt template for natal chart interpretation.
        
        Returns:
            Prompt template string
        """
        return """
        You are an expert astrologer tasked with interpreting a natal chart.
        Below is the data from the chart:
        
        Report Title: {title}
        
        Birth Data:
        {data_table}
        
        Planet Positions:
        {planets_table}
        
        House Positions:
        {houses_table}
        
        Full Report Text (for context if needed):
        ---
        {full_report}
        ---
        
        Please provide a {tone} interpretation of this chart, focusing on: {focus_areas}.
        Your interpretation should be {max_length_text}.
        
        Structure your response using Markdown with the following headings. Use appropriate subheadings (e.g., ###) and bullet points (*) or numbered lists where helpful:
        
        # Natal Chart Interpretation for {title}
        
        ## Overall Chart Signature
           - [Provide a 1-2 paragraph overview of the dominant energies, core themes, and the individual's general life approach based on the chart.]
        
        ## Key Astrological Themes
           - **[Identify and name the first major theme, e.g., "Emotional Depth & Intuition"]:**
             - [Explain this theme, linking it to specific placements like Grand Trines, stelliums, or dominant elements/modalities. Discuss its potential positive and challenging manifestations.]
           - **[Identify and name the second major theme, e.g., "Drive for Self-Expression & Leadership"]:**
             - [Explain this theme, linking it to relevant placements. Discuss its potential positive and challenging manifestations.]
           - **[Identify and name a third major theme if applicable, e.g., "Tension between Idealism and Reality"]:**
             - [Explain this theme, linking it to challenging aspects or configurations. Discuss its potential positive and challenging manifestations.]
        
        ## Planetary Placements
           - **Sun in [Sign] ([Nth] House):** [Interpret the Sun's sign, house, and any immediate, very strong aspects it makes.]
           - **Moon in [Sign] ([Nth] House):** [Interpret the Moon's sign, house, and any immediate, very strong aspects it makes.]
           - (Continue for Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Ascendant, Midheaven)
        
        ## Significant House Placements & Stelliums
           - **[Nth] House in [Sign] (with [Planet A, Planet B] if a stellium):**
             - [Interpret the significance of this house, including any planets residing within it, especially if it forms a stellium. Discuss the life areas affected.]
           - (Repeat for other houses with significant placements or stelliums)
        
        ## Major Aspect Patterns
           - **[Aspect Pattern Name, e.g., Water Grand Trine (Moon, Jupiter, Pluto in Scorpio)]:**
             - [Detailed interpretation of this major aspect pattern, its gifts, and potential challenges.]
           - **[Challenging Aspect, e.g., Saturn-Neptune Square]:**
             - [Detailed interpretation of this significant challenging aspect, its lessons, and how to navigate it.]
           - (Discuss 1-2 other highly significant aspects if present)
        
        ## Summary: Strengths & Challenges
           - **Key Strengths:**
             * [Strength 1 derived from the analysis]
             * [Strength 2 derived from the analysis]
           - **Potential Challenges:**
             * [Challenge 1 derived from the analysis]
             * [Challenge 2 derived from the analysis]
        
        ## Practical Guidance & Suggestions
           * [Actionable suggestion 1 based on the chart's themes and challenges.]
           * [Actionable suggestion 2 based on the chart's themes and challenges.]
        
        ## Conclusion
           - [Provide a brief concluding paragraph summarizing the chart's essence and potential for growth.]
           - *Disclaimer: Astrological interpretations offer insights and potentials, not fixed destinies. Personal growth and conscious choices play a significant role in shaping one's life.*
        """
    
    def _get_synastry_prompt_template(self) -> str:
        """
        Get the prompt template for synastry chart interpretation.
        
        Returns:
            Prompt template string
        """
        return """
        You are an expert astrologer tasked with interpreting a synastry chart comparison.
        Below is the data from both natal charts:
        
        Person 1:
        ----------
        {person1_title}
        
        Birth Data:
        {person1_data_table}
        
        Planet Positions:
        {person1_planets_table}
        
        House Positions:
        {person1_houses_table}
        
        Person 2:
        ----------
        {person2_title}
        
        Birth Data:
        {person2_data_table}
        
        Planet Positions:
        {person2_planets_table}
        
        House Positions:
        {person2_houses_table}
        
        Synastry Aspects:
        {aspects_table}
        
        Please provide a {tone} interpretation of the relationship dynamics between these two individuals,
        focusing on: {focus_areas}
        
        Your interpretation should be {max_length_text} and should highlight the most significant patterns 
        and potential areas of harmony and tension in the relationship.
        
        Structure your response using Markdown with appropriate headings, subheadings, bullet points, and formatting.
        """ 