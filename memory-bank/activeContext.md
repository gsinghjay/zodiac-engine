# Active Context: Zodiac Engine

## Current Focus

- **HTMX Implementation**: Plan to integrate HTMX with our web interface to create a more dynamic and responsive user experience without heavy JavaScript.
- **Troubleshooting Configuration**: Investigating why the `GEONAMES_USERNAME` setting is not being correctly read from the `.env` file, despite being set by the user.
- **Web Interface Functional**: The web interface itself is functional, but the GeoNames integration (used for city lookups and timezone) is failing due to the configuration issue.
- **Prepare for Next Phase**: The major refactoring effort (FastAPI best practices, API structure migration) is complete. All 25 tests are passing.
- **Planning**: Reviewing the `Natal Chart Expansion Plan` (`docs/natal-chart-expansion-plan.md`) to prepare for implementation.

## Recent Changes

- **Router Structure Consolidation**:
  - Addressed the inconsistent router structure where web routes were in `app/routers/` while API routes were in `app/api/v1/routers/`.
  - Moved all web routes from `app/routers/web.py` to `app/api/web.py`.
  - Updated imports in `app/api/__init__.py` to include the web router.
  - Removed references to the old web router from `app/main.py`.
  - Removed the obsolete `app/routers/` directory.
  - Confirmed all 25 tests continue to pass after the changes.
  - This brings the codebase in line with FastAPI best practices by keeping all routes under the `app/api/` directory.

- **GeoNames Debugging**:
  - Analyzed `app/core/config.py` and `app/services/geo_service.py` to understand how settings are loaded and used.
  - Confirmed `pydantic-settings` is configured to read `.env`.
  - Added debug logging to `GeoService.__init__` to print the value of `settings.GEONAMES_USERNAME` as read by Pydantic.
  - Logs confirmed the value is being read as an empty string, leading to the use of the demo account and API errors.
  - Updated `GeoService.__init__` to handle empty strings explicitly and improve logging around username usage.
  - Identified potential causes: `.env` file path issues, file format/encoding problems, environment variable overrides, or unexpected Pydantic behavior.

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
  - All 25 tests confirmed passing after refactoring and migration.

- **Memory Bank Initialization**: Previously created initial versions of all core Memory Bank files.

## Next Steps

1. **Implement HTMX Integration**:
   * Add HTMX library to the layout.html template
   * Create HTML fragment templates for partial updates
   * Update existing routes to handle HTMX requests
   * Add HTMX attributes to forms and UI elements
   * Implement key features:
     * Live location search with HTMX
     * Real-time chart preview as options change
     * Form validation with instant feedback
     * Improved tab switching
     * Progress indicators for chart generation
     
2. **Resolve .env Issue**: Assist the user in applying one of the suggested solutions:
    * Recreate the `.env` file with correct formatting/encoding.
    * Temporarily export the `GEONAMES_USERNAME` variable in the shell.
    * Modify `config.py` to use an absolute path for `env_file`.
    
3. **Verify Fix**: Once a solution is applied, run the application and check the logs to confirm `GEONAMES_USERNAME` is read correctly and the GeoNames API calls succeed.
    
4. **Implement Natal Chart Expansion Plan**: After HTMX integration and configuration fixes, proceed with the features detailed in `docs/natal-chart-expansion-plan.md`. Prioritize:
   - Enhanced Planet/House Info (Schema updates, Service logic)
   - Element/Quality Analysis (Schema updates, Service logic)
   - Lunar Phase Info (Schema updates, Service logic)
   
5. **Future Feature Development**: Defer work on other features (transit calculations, LLM interpretations) until after the natal chart expansion core items are addressed.

## Active Decisions & Considerations

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
- **.env Loading**: Investigating the reliability of `pydantic-settings` reading `.env` files in the current setup.
- **Error Handling**: Ensured `GeoService` logs appropriate warnings/errors based on the `GEONAMES_USERNAME` value.

## Important Patterns & Preferences

- **Web Interface**: Server-side rendering with Jinja2 templates and modern CSS for the UI.
- **Follow Best Practices**: Adhere to documented FastAPI best practices.
- **Modularity**: Maintain clear separation of concerns between API, service, and core layers.
- **Documentation**: Keep project documentation up-to-date with changes.
- **Testing**: Ensure changes maintain or improve test coverage.
- **Type Safety**: Use proper typing and Pydantic validation throughout the codebase.
- **Environment Configuration**: Single source of truth in .env files with proper parsing in Settings.
- **Status Code Constants**: Use FastAPI status code constants instead of hardcoded values.

## Learnings & Insights

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
- Thorough testing during refactoring is critical for catching regressions (e.g., the `SiderealMode` case sensitivity).
- Git `mv` is useful for preserving history during file structure changes.
- The Pydantic v2 syntax is more concise and readable compared to v1.
- Proper dependency injection with instance methods provides better testability and maintainability.
- Using status code constants from FastAPI improves code readability and maintainability.
- Documenting environment variables is crucial for new developers to set up the project correctly.
- Property methods in Pydantic Settings classes provide a clean way to transform string configuration values into more complex types.
- When working with Literal types for validation, the exact string format (case, spacing) must match the definition in the schema.
- Regular testing during refactoring is essential to catch issues early, as demonstrated by our discovery and fix of the sidereal mode test.
- Debugging configuration loading requires inspecting both the loading mechanism (`pydantic-settings`) and how the setting is used (`GeoService`).
- Empty strings in environment variables or `.env` files can lead to unexpected behavior if not handled explicitly.
- Direct confirmation of the value being read (via logging) is crucial for diagnosing configuration issues.
- Potential inconsistencies between system environment variables and `.env` file variables need to be considered. 