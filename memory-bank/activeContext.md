# Active Context: Zodiac Engine

## Current Focus

- **UI Enhancement with Bootstrap**: Migrated the web interface from custom CSS to Bootstrap for improved responsiveness and consistency.
- **Dedicated Chart Details Page**: Implemented a dedicated page for chart viewing with download options.
- **Web Interface Optimization**: Simplifying the user interface by removing the preview chart feature and focusing on the primary chart generation functionality.
- **Bug Fixes & Improvements**: Resolving issues with house system mappings and language code handling to ensure correct chart generation.
- **HTMX Implementation**: Plan to integrate HTMX with our web interface to create a more dynamic and responsive user experience without heavy JavaScript.
- **Web Interface Functional**: The web interface is now fully functional, with improvements to error handling and configuration issues resolved.
- **Prepare for Next Phase**: The major refactoring effort (FastAPI best practices, API structure migration) is complete. All tests are passing.
- **Planning**: Reviewing the `Natal Chart Expansion Plan` (`docs/natal-chart-expansion-plan.md`) to prepare for implementation.

## Recent Changes

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
  - Implemented download options for different file formats (SVG, PNG, PDF)
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

- **GeoService Improvements**:
  - Fixed an issue where `GeoService` was calling a non-existent `search_city` method.
  - Renamed the method call to `search_cities` to match the actual implementation.
  - Made the `search_cities` and `_get_timezone` methods asynchronous to properly work with the async route handlers.
  - Added appropriate `await` keyword to method calls.
  - This resolves errors in the location search functionality.

- **Web Interface Added**:
  - Created a user-friendly web interface with FastAPI and Jinja2 templates.
  - Implemented tabs for Western (Tropical) and Vedic (Sidereal) chart generation.
  - Added form-based input for birth details and chart configuration.
  - Integrated with existing chart visualization service for SVG generation.
  - Added responsive design with modern CSS styling.
  - Implemented background task processing for chart generation.
  - Fixed duplicate dependencies in requirements.txt.

- **Refactoring Complete**:
  - Successfully implemented all FastAPI best practices outlined previously.
  - Successfully migrated API structure from `endpoints/` to `routers/`.
  - Updated dependencies, configuration, services (instance methods/DI), Pydantic models (v2), tests, error handling, and response codes/models.
  - Ensured async/sync consistency.
  - All tests confirmed passing after refactoring and migration.

## Next Steps

1. **Enhance Download Options**:
   * Implement actual SVG to PNG conversion functionality
   * Implement SVG to PDF conversion functionality
   * Add proper file type detection and content-type headers

2. **Chart Data Persistence**:
   * Implement a more robust solution for chart data persistence beyond the in-memory cache
   * Consider using a database for storing chart data and user preferences
   * Add expiration times for generated charts
   
3. **UI Improvements**:
   * Add more interactive elements using Bootstrap's components
   * Improve mobile responsiveness
   * Enhance form validation with clearer error messages
   * Add tooltips for chart options and configurations
   
4. **Implement Natal Chart Expansion Plan**: Proceed with the features detailed in `docs/natal-chart-expansion-plan.md`. Prioritize:
   - Enhanced Planet/House Info (Schema updates, Service logic)
   - Element/Quality Analysis (Schema updates, Service logic)
   - Lunar Phase Info (Schema updates, Service logic)
   
5. **Future Feature Development**: Defer work on other features (transit calculations, LLM interpretations) until after the natal chart expansion core items are addressed.

## Active Decisions & Considerations

- **Bootstrap vs Custom CSS**: Chose Bootstrap for its comprehensive component library, strong community support, and built-in responsiveness.
- **Dedicated Chart Page**: Decided to create a separate page for chart viewing to provide more space for the chart and additional options.
- **Download Options**: Offering different file formats (SVG, PNG, PDF) to accommodate various user needs.
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