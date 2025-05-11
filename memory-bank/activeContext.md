# Active Context: Zodiac Engine

## Current Focus

- **LLM Interpretation API Integration**: Implementing integration with LLM providers (Gemini/Anthropic/OpenAI) for the chart interpretation service.
- **LLM API Selection**: Configuring environment variables for chosen LLM provider and setting up caching strategy.
- **UI Implementation Complete**: Successfully implemented the frontend elements for chart interpretation, including options customization and HTMX integration.
- **API Endpoints Complete**: Successfully created the API structure for both report generation and interpretation services.
- **Report Generation Framework**: Successfully implemented report generation service using Kerykeion's Report class for formatted tabular data.
- **Fragment Templates**: Created template fragments for displaying interpretation results and formatted reports.
- **Environment Configuration for LLM**: Created settings structure for LLM API keys and model selection with appropriate defaults.
- **SVG Conversion Implementation**: Successfully implemented SVG to PNG, PDF, and JPEG conversion for chart downloads using CairoSVG and Pillow libraries.
- **CSS Variable Preprocessing**: Created utilities to handle CSS variables in SVG files before conversion to ensure proper rendering across all formats.
- **Download Options Enhancement**: Updated the chart download endpoint to support multiple formats with appropriate content types and file extensions.
- **UI Enhancement with Bootstrap**: Migrated the web interface from custom CSS to Bootstrap for improved responsiveness and consistency.
- **Dedicated Chart Details Page**: Implemented a dedicated page for chart viewing with download options.
- **Web Interface Optimization**: Simplifying the user interface by removing the preview chart feature and focusing on the primary chart generation functionality.
- **Bug Fixes & Improvements**: Resolving issues with house system mappings and language code handling to ensure correct chart generation.
- **HTMX Integration**: Successfully integrated HTMX with our web interface to create a more dynamic and responsive user experience without heavy JavaScript.
- **Web Interface Functional**: The web interface is now fully functional, with improvements to error handling and configuration issues resolved.
- **Prepare for Next Phase**: The major refactoring effort (FastAPI best practices, API structure migration) is complete. All tests are passing.
- **Planning**: Reviewing the `Natal Chart Expansion Plan` (`docs/natal-chart-expansion-plan.md`) to prepare for implementation.
- **Roadmap Reprioritization**: Updated the project roadmap to prioritize API structure reorganization and SQLite-based data persistence.

## Recent Changes

- **Chart Interpretation UI Implementation**:
  - Updated the chart_details.html template to include interpretation and report sections
  - Added HTMX-powered buttons for generating interpretations with customization options
  - Created form inputs for customizing interpretation focus areas, tone, and length
  - Added loading indicators for LLM processing
  - Created a print-friendly option for interpretations and reports
  - Added responsive layout for both mobile and desktop views

- **Interpretation Fragment Template**:
  - Created template fragment at app/templates/fragments/interpretation.html
  - Implemented sections for main interpretation text, key highlights, and suggestions
  - Added error handling for failed interpretations
  - Styled with Bootstrap for consistent appearance

- **Report Fragment Template**:
  - Created template fragment at app/templates/fragments/report.html
  - Implemented sections for birth data, planet positions, and house positions
  - Added monospace formatting for ASCII tables
  - Added download and print options for reports
  - Styled with Bootstrap for consistent appearance

- **Web Routes for Interpretation**:
  - Added /interpret-chart/{chart_id} endpoint for generating interpretations
  - Added /chart-report/{chart_id} endpoint for generating reports
  - Added /download-report/{chart_id} endpoint for downloading full reports
  - All endpoints support HTMX for dynamic content loading
  - Implemented proper error handling with user-friendly messages

- **API Endpoints Creation**:
  - Created new router at app/api/v1/routers/charts/interpretations.py
  - Implemented /api/v1/charts/interpretations/natal endpoint
  - Implemented /api/v1/charts/interpretations/synastry endpoint
  - Added comprehensive validation and detailed error responses
  - Added the interpretations router to the charts router

- **Settings Configuration**:
  - Updated Settings class in app/core/config.py to include LLM configuration
  - Added configuration for LLM API key, model name, provider, and caching options
  - Added llm_config property method for easy access to all LLM settings
  - Updated README with LLM configuration instructions

- **Dependency Injection**:
  - Added InterpretationServiceDep to app/core/dependencies.py
  - Implemented factory method for InterpretationService with settings dependency
  - Updated web.py routes to use the new dependency

- **Report Generation Service Implementation**:
  - Created a new `ReportService` class in `app/services/report.py` to generate formatted astrological reports
  - Implemented methods for both natal and synastry report generation
  - Integrated with Kerykeion's Report class to generate tabular ASCII reports
  - Set up proper error handling and logging
  - Added dependency injection for the service in `app/core/dependencies.py`

- **Report API Endpoints Implementation**:
  - Created a new router at `app/api/v1/routers/charts/reports.py` for report-related endpoints
  - Implemented `/api/v1/charts/reports/natal` endpoint for generating natal chart reports
  - Implemented `/api/v1/charts/reports/synastry` endpoint for generating synastry reports
  - Added comprehensive validation and error handling
  - Updated the charts router to include the new reports router

- **Report Schemas Creation**:
  - Created schema definitions in `app/schemas/report.py` for request/response models
  - Implemented request validation schemas with proper documentation
  - Created response models for both natal and synastry reports
  - Added examples and type annotations for better API documentation
  - Created schemas for future LLM interpretation requests/responses

- **LLM Interpretation Placeholder**:
  - Created `InterpretationService` class in `app/services/interpretation.py` as a placeholder for LLM integration
  - Implemented prompt template methods for different chart types
  - Added parameter preferences to customize interpretations based on user needs
  - Created methods for both natal and synastry chart interpretations
  - Set up structure to support different LLM providers (Gemini/Anthropic/OpenAI)

- **SVG Conversion Implementation**:
  - Created a new `FileConversionService` class in `app/services/file_conversion.py` to handle SVG conversion to different formats
  - Implemented conversion to PNG, PDF, and JPEG formats using CairoSVG and Pillow libraries
  - Added proper error handling with a custom `FileConversionError` exception
  - Set up dependency injection for the service in `app/core/dependencies.py`
  - Implemented content type mapping for HTTP responses
  - Added support for configurable DPI (dots per inch) for raster formats

- **CSS Variable Preprocessing**:
  - Implemented utilities in `app/core/svg_utils.py` to handle CSS variables in SVG files
  - Created functions to parse variables from SVG content, resolve nested variable references, and substitute them with actual values
  - Ensured SVG files render correctly across all output formats

- **Download Chart Endpoint Enhancement**:
  - Updated the `/download-chart/{chart_id}` endpoint to use our new conversion service
  - Added support for SVG, PNG, PDF, and JPEG formats with proper content-type headers
  - Implemented a DPI query parameter for controlling resolution of raster formats
  - Added documentation about the DPI option in the chart details template
  - Fixed issues with proper file reading and handling

- **HTMX Implementation**:
  - Added HTMX library to the layout.html template
  - Created dedicated HTMX endpoints for dynamic content loading
  - Implemented location search with real-time results using hx-get
  - Added form validation with instant feedback using hx-post
  - Created partial templates for HTMX-powered updates
  - Implemented smooth transitions for UI state changes with CSS
  - Enhanced the chart details page with real-time data refresh
  - Maintained progressive enhancement by ensuring functionality works without JavaScript

- **Bootstrap Implementation**:
  - Replaced most custom CSS with Bootstrap classes
  - Added Bootstrap CSS and JS to the layout.html file
  - Updated form elements with Bootstrap's form-control classes
  - Implemented Bootstrap's grid system for responsive layout
  - Improved tab navigation using Bootstrap's tab component
  - Created a minimal custom CSS file that only contains necessary overrides
  - Maintained the same color scheme and design aesthetics

- **Dedicated Chart Details Page**:
  - Created a new chart_details.html template with a two-column layout
  - Implemented a chart display section with high-quality SVG rendering
  - Added a detailed information section showing chart data
  - Implemented download options for different file formats (SVG, PNG, PDF, JPEG)
  - Added a share functionality with copyable URL
  - Enhanced navigation with a "Back to Generator" button

- **Chart Generation Flow Improvement**:
  - Modified the generate_chart endpoint to redirect to the dedicated chart details page
  - Implemented a chart data cache for storing chart information
  - Added proper error handling for the chart generation process
  - Enhanced the user experience by showing loading indicators during chart generation

- **Bug Fixes**:
  - Fixed routing issues by adding proper route names to API endpoints
  - Resolved template rendering errors by using direct URL paths instead of url_for in templates
  - Fixed the missing chart_preview.html template issue

- **Preview Chart Removal**:
  - Removed the preview chart feature to simplify the user interface and reduce server load.
  - Deleted the `/preview-chart` endpoint from the API.
  - Removed preview buttons and related UI elements from the template.
  - Deleted the chart preview template fragment.
  - Updated placeholder text for chart result area.
  - This change streamlines the user experience by focusing on the primary chart generation.

- **Fixed House System Mapping**:
  - Added a mapping system to convert human-readable house system names (like "Whole Sign") to their corresponding single-letter codes (like "W") required by the Kerykeion library.
  - Created `HOUSE_SYSTEM_MAP` dictionary and `map_house_system()` function in the chart visualization service.
  - Added logging to track the house system mapping for debugging purposes.
  - Updated documentation in route handlers to explain the mapping.
  - This fixes the error: `'Whole Sign' is NOT a valid house system!` that was preventing chart generation.

- **Fixed Language Code Handling**:
  - Updated chart generation methods to convert language codes to uppercase (e.g., "en" to "EN") as required by the Kerykeion library.
  - Added logging to track the language code conversion.
  - Updated documentation in route handlers to explain the conversion.
  - This fixes the `KeyError: 'en'` error that was occurring during chart generation.

- **Router Structure Consolidation**:
  - Addressed the inconsistent router structure where web routes were in `app/routers/` while API routes were in `app/api/v1/routers/`.
  - Moved all web routes from `app/routers/web.py` to `app/api/web.py`.
  - Updated imports in `app/api/__init__.py` to include the web router.
  - Removed references to the old web router from `app/main.py`.
  - Removed the obsolete `app/routers/` directory.
  - Confirmed all tests continue to pass after the changes.
  - This brings the codebase in line with FastAPI best practices by keeping all routes under the `app/api/` directory.

## Next Steps

1. **LLM API Integration** (HIGHEST PRIORITY):
   * Choose and implement actual LLM API integration (Anthropic Claude, OpenAI GPT-4, or Google Gemini)
   * Update the InterpretationService to use the selected LLM API
   * Test with actual API keys to ensure proper functioning
   * Implement caching for LLM responses to reduce API costs
   * Create error handling for API rate limits and failures
   * Document the required environment variables for LLM setup

2. **Testing for Interpretation**:
   * Create comprehensive unit tests for the InterpretationService
   * Test with mock LLM responses to avoid API costs during testing
   * Implement integration tests for the interpretation endpoints
   * Create test fixtures with sample report data
   * Test the interpretation UI with Selenium or similar tools

3. **API Structure Reorganization**:
   * Move `app/api/web.py` into a dedicated web folder (`app/api/web/`)
   * Split web.py into logical components (chart generation, location search, download functionality)
   * Update imports in `app/api/__init__.py` to reflect the new structure
   * Ensure all tests continue to pass after the reorganization
   * This will improve code organization and maintainability by grouping related functionality

4. **Chart Data Persistence with SQLite**:
   * Implement SQLite database for storing chart data and user preferences
   * Create appropriate database models and migration scripts using SQLAlchemy
   * Add expiration times for generated charts
   * Implement database connection pooling and proper error handling
   * Create a data access layer with repository pattern for chart data

5. **UI Improvements**:
   * Add more interactive elements using Bootstrap's components
   * Improve mobile responsiveness
   * Enhance form validation with clearer error messages
   * Add tooltips for chart options and configurations
   
6. **Extend HTMX Implementation**:
   * Add more sophisticated HTMX patterns for complex interactions
   * Implement websockets for real-time updates using HTMX's SSE support
   * Create more partial templates for dynamic content loading
   * Add animation effects for state transitions
   
7. **Implement Natal Chart Expansion Plan**: Proceed with the features detailed in `docs/natal-chart-expansion-plan.md`. Prioritize:
   - Enhanced Planet/House Info (Schema updates, Service logic)
   - Element/Quality Analysis (Schema updates, Service logic)
   - Lunar Phase Info (Schema updates, Service logic)

## Active Decisions & Considerations

- **LLM Provider Selection**: Considering the trade-offs between OpenAI GPT-4, Anthropic Claude, and Google Gemini models. Each has different strengths for astrological knowledge, with cost and performance considerations.
- **LLM API Error Handling**: Designing robust error handling for LLM API failures, with graceful degradation and helpful user feedback.
- **Caching Strategy**: Planning to implement caching for LLM responses to reduce API costs, with consideration for cache invalidation on report data changes.
- **Prompt Engineering**: Refining prompt templates for astrological interpretation to get consistently high-quality results from the selected LLM.
- **Response Formatting**: Ensuring LLM responses have consistent structure for proper display in the UI, potentially using output parsers.

- **LLM Integration Approach**: Planning to support multiple LLM providers (primarily Anthropic/Claude and Google Gemini) to give users flexibility, with clear configuration options.
- **Interpretation Customization**: Will allow users to customize interpretations based on focus areas (planets, houses, aspects) and tone (beginner-friendly, detailed, etc.).
- **Prompt Engineering**: Creating specific prompt templates for astrological interpretation that leverage the Report output format for consistent results.
- **Frontend Integration**: Using HTMX for the interpretation UI to maintain our progressive enhancement approach without heavy JavaScript.
- **Interpretation Privacy**: Ensuring any data sent to LLM providers is anonymized appropriately and users are informed about data usage.
- **Error Handling**: Implementing robust error handling for API failures, with graceful fallbacks if the LLM service is unavailable.
- **Cost Management**: Designing the system to be mindful of LLM API costs through appropriate caching and request optimization.

- **File Conversion Approach**: Chose CairoSVG as the primary conversion solution due to its excellent support for SVG standards and Pillow for additional JPEG conversion capability.
- **CSS Variable Handling**: Implemented a preprocessing approach for CSS variables rather than relying on the SVG libraries to handle them natively, as many conversion libraries don't fully support modern CSS features.
- **DPI Configuration**: Made DPI configurable via a query parameter to allow users to control the quality and file size of raster outputs.
- **Error Handling**: Created a dedicated error type for file conversion issues to provide clear feedback to users.
- **Bootstrap vs Custom CSS**: Chose Bootstrap for its comprehensive component library, strong community support, and built-in responsiveness.
- **Dedicated Chart Page**: Decided to create a separate page for chart viewing to provide more space for the chart and additional options.
- **Download Options**: Offering different file formats (SVG, PNG, PDF, JPEG) to accommodate various user needs.
- **Direct URL Paths**: Using direct URL paths in templates to avoid routing issues with url_for.
- **In-Memory Cache**: Currently using a simple dictionary for chart data storage as a quick solution, with plans to implement a more robust solution later.
- **UI Simplification**: Removed the preview chart feature to focus on the core functionality and reduce complexity.
- **Library Compatibility**: Added mappings and conversions to ensure compatibility with the Kerykeion library's expected input formats.
- **Error Logging**: Enhanced logging to help identify and troubleshoot issues.
- **HTMX Integration Strategy**: Using HTMX for progressive enhancement of the existing server-rendered templates rather than rebuilding the interface with a JavaScript framework.
- **Web Interface Architecture**: Using FastAPI's template support with Jinja2 for server-side rendering rather than a separate frontend framework.
- **Responsive Design**: The web interface is designed to work on both desktop and mobile devices.
- **Background Processing**: Using FastAPI's background tasks for chart generation to improve user experience.
- **Refactoring Adherence**: All implemented changes followed the defined FastAPI best practices and migration plan.
- **Modern DI**: Utilizing Annotated types and factory functions for dependency injection is the standard.
- **Pydantic v2**: V2 syntax is the standard for all new/updated schemas.
- **Service Layer**: Instance methods with DI are the standard pattern for services.
- **Configuration**: `.env` file via Pydantic `Settings` is the standard.
- **Testing**: Maintaining comprehensive test coverage with `pytest` is crucial.
- **Error Handling**: Ensuring services log appropriate warnings/errors to aid debugging.

## Important Patterns & Preferences

- **LLM Integration**: Use dependency injection for LLM service configuration, with appropriate factory methods in core/dependencies.py.
- **Environment Variables**: Use pydantic-settings for LLM API keys and configuration, following the existing pattern for sensitive values.
- **Prompt Templates**: Maintain prompt templates as methods within the InterpretationService class to keep them organized and maintainable.
- **Response Formatting**: Format LLM responses consistently with other API responses, using Pydantic models to validate structure.
- **Error Boundaries**: Implement specific exception types for LLM-related errors to provide clear error messages to users.
- **Caching**: Use an appropriate caching strategy for LLM responses to reduce API costs and improve performance.

- **SVG Conversion**: Use CairoSVG for primary conversion and Pillow for additional formats like JPEG when needed.
- **CSS Variable Handling**: Use regex-based preprocessing to handle modern CSS features that might not be supported by conversion libraries.
- **Download Experience**: Provide multiple download formats with proper content types and meaningful filenames.
- **Bootstrap Integration**: Use Bootstrap classes for layout and components, with minimal custom CSS only for specific overrides.
- **Responsive Design**: Ensure all pages work well on various device sizes using Bootstrap's grid system and responsive utilities.
- **Page Structure**: Maintain a consistent structure across pages with proper heading hierarchy and navigation.
- **Component Reuse**: Use template fragments to reuse common components across different pages.
- **Progressive Enhancement**: Build a solid base experience that works without JavaScript, then enhance with interactive features.
- **Web Interface**: Server-side rendering with Jinja2 templates and modern CSS for the UI.
- **Follow Best Practices**: Adhere to documented FastAPI best practices.
- **Modularity**: Maintain clear separation of concerns between API, service, and core layers.
- **Documentation**: Keep project documentation up-to-date with changes.
- **Testing**: Ensure changes maintain or improve test coverage.
- **Type Safety**: Use proper typing and Pydantic validation throughout the codebase.
- **Environment Configuration**: Single source of truth in .env files with proper parsing in Settings.
- **Status Code Constants**: Use FastAPI status code constants instead of hardcoded values.
- **Mapping Functions**: Use mapping functions for converting between user-friendly values and library-required formats.

## Learnings & Insights

- **Frontend Preparation First**: Implementing the UI components before the actual LLM integration allows for testing with placeholder data and ensures a smooth user experience.
- **HTMX Advantages for LLM UIs**: HTMX's approach to progressive enhancement is particularly well-suited for LLM applications, as it handles the loading states and asynchronous updates gracefully.
- **Modular Template Structure**: Using template fragments for interpretation and report display makes the code more maintainable and enables reuse.
- **Interpretation Options Value**: Giving users control over their interpretation focus (planets, houses, aspects) and tone provides a more personalized experience.
- **Environment-First Development**: Setting up the configuration infrastructure before implementing the actual API integration makes testing easier and enables quick switching between providers.

- **LLM Integration Considerations**: Implementing the Report service first gives us structured data that can be more easily passed to LLM APIs for interpretation.
- **Astrological Interpretation Complexity**: The depth of astrological interpretation requires careful prompt engineering to get meaningful results from LLMs.
- **User Experience Focus**: LLM interpretation adds significant value to the user experience, making it worth prioritizing ahead of some infrastructure improvements.
- **Report Generation Efficiency**: Kerykeion's built-in Report class provides an efficient way to generate formatted tabular data that's both human-readable and machine-parseable.
- **Progress Through Layers**: Our layered approach (from Service to API to UI) continues to be effective for implementing new features.

- **SVG Conversion Complexity**: Converting SVG to other formats involves handling CSS variables and ensuring consistent rendering across different libraries.
- **CairoSVG Capabilities**: CairoSVG provides excellent SVG rendering but requires preprocessing of modern CSS features like variables.
- **Multi-format Support**: Offering multiple download formats enhances user experience by accommodating different use cases.
- **DPI Considerations**: For raster formats, allowing configurable DPI gives users control over the quality/file size tradeoff.
- **HTMX Benefits**: HTMX provides a lightweight way to add dynamic behavior to web applications without complex JavaScript frameworks, making it ideal for enhancing server-rendered templates.
- **Progressive Enhancement**: Building features that work without JavaScript first, then enhancing with HTMX, creates a more resilient application.
- **Partial Templates**: Creating small, focused template fragments for HTMX to load dynamically improves code organization and reusability.
- **Backend Integration**: HTMX shifts complexity from client-side JavaScript to server-side endpoints, leveraging our existing FastAPI knowledge.
- **Transition Effects**: Simple CSS transitions triggered by HTMX attributes create a polished user experience with minimal effort.
- **Bootstrap Integration**: Migrating to Bootstrap can significantly reduce the amount of custom CSS needed while providing a more consistent and responsive UI.
- **Chart Details Page**: A dedicated page for chart viewing provides a better user experience than inline previews, especially for complex data visualization.
- **In-Memory Caching**: Simple dictionary-based caching can be effective for prototyping but has limitations for production use (no persistence across restarts, memory issues with many entries).
- **FastAPI Routing**: Named routes are essential when using url_for in templates, but direct URL paths can be a simpler alternative.
- **Template Debugging**: Errors in templates can be challenging to debug; using direct paths can help isolate issues.
- **Library Compatibility**: When integrating with external libraries (like Kerykeion), it's important to understand their expected input formats and create proper mappings/conversions.
- **UI Simplification**: Removing non-essential features can improve both the user experience and reduce server load.
- **Proper Error Handling**: Comprehensive error handling with appropriate logging is essential for diagnosing issues in production.
- **Asynchronous Consistency**: Ensuring all async methods are properly defined with `async def` and called with `await` is critical for preventing runtime errors.
- **Documentation Importance**: Documenting mappings and conversions helps future developers understand why certain transformations are necessary.
- Router structure organization is critical for maintaining a consistent and maintainable FastAPI application.
- Consolidating routes under a single directory tree (`app/api/`) improves code organization and follows FastAPI best practices.
- FastAPI's integration with Jinja2 templates provides a straightforward way to build web interfaces without a separate frontend framework.
- Background tasks in FastAPI are effective for handling long-running operations like chart generation.
- Proper SVG directory initialization is important to prevent file access errors when saving generated charts.
- Consistent error handling in the web interface improves user experience.
- CSS variables provide an easy way to maintain a consistent design system across the interface.
- Refactoring significantly improved code structure, testability, and adherence to modern standards.
- The migration to the `routers/` structure enhances organization.
- Pydantic v2 and modern DI patterns are effective.
- Property methods in `Settings` are useful for type coercion.
- Instance methods in services simplify DI and testing.
- Consistent use of status constants is beneficial.
- Thorough testing during refactoring is critical for catching regressions.
- Git `mv` is useful for preserving history during file structure changes.
- Using status code constants from FastAPI improves code readability and maintainability.
- Documenting environment variables is crucial for new developers to set up the project correctly.
- Property methods in Pydantic Settings classes provide a clean way to transform string configuration values into more complex types.
- When working with Literal types for validation, the exact string format (case, spacing) must match the definition in the schema.
- Debugging configuration loading requires inspecting both the loading mechanism (`pydantic-settings`) and how the setting is used.
- Empty strings in environment variables or `.env` files can lead to unexpected behavior if not handled explicitly.
- Direct confirmation of the value being read (via logging) is crucial for diagnosing configuration issues. 