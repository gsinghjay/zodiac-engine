# CHANGELOG


## v0.7.0 (2025-05-16)

### Chores

- Update README.md with chart generation form on mobile
  ([`680f50b`](https://github.com/gsinghjay/zodiac-engine/commit/680f50ba072cf061cb3fe592b7ece7ab33aff848))

### Code Style

- Update styles with cosmic gradient theme
  ([`3d76d39`](https://github.com/gsinghjay/zodiac-engine/commit/3d76d396d8d7bdac6eddf1a157073539e0de8ec3))

### Documentation

- Update memory bank with landing page implementation details
  ([`21f4fbe`](https://github.com/gsinghjay/zodiac-engine/commit/21f4fbe3dc55e0e150f1225b9e49a8a064810a72))

### Features

- Add AI interpretation illustration for landing page
  ([`5895046`](https://github.com/gsinghjay/zodiac-engine/commit/58950466de1c44813ed27f795bed392f77f1ba9d))

- Add animated cosmic background SVG for hero section
  ([`5c6f3fd`](https://github.com/gsinghjay/zodiac-engine/commit/5c6f3fd69de08ca972662040705c21eebdd041a2))

- Add landing page with cosmic-themed hero section
  ([`5e0c6db`](https://github.com/gsinghjay/zodiac-engine/commit/5e0c6dbb55215bd4dddee3d08570b6d48024d29e))

- Add navigation and gradient header to layout template
  ([`3e0701a`](https://github.com/gsinghjay/zodiac-engine/commit/3e0701ac04170a317c7387ad75df8e814f0124fa))

- Update routes to make landing page the root URL
  ([`5b4bb53`](https://github.com/gsinghjay/zodiac-engine/commit/5b4bb53ae094702b8cb0108222f7ed87130f2195))


## v0.6.1 (2025-05-16)

### Bug Fixes

- Process CSS variable defaults in SVG files when no variables provided
  ([`2aa644a`](https://github.com/gsinghjay/zodiac-engine/commit/2aa644a55ae7da213851738f0595a7962eae141b))

### Chores

- Remove unused processed SVG file
  ([`90a2ecb`](https://github.com/gsinghjay/zodiac-engine/commit/90a2ecb2a4a80b993e2797c17c36bc26d0a86c52))

### Documentation

- Enhance README with architecture diagrams and explanations
  ([`71c4935`](https://github.com/gsinghjay/zodiac-engine/commit/71c493555ec6b1de4940eb5a9cfb963934d3823b))

### Refactoring

- Rename test script to avoid pytest collection conflicts
  ([`189d507`](https://github.com/gsinghjay/zodiac-engine/commit/189d5078905bd1d0762183cd89bb8c5a01874579))


## v0.6.0 (2025-05-11)

### Chores

- Remove unused repomix output file
  ([`65e81cb`](https://github.com/gsinghjay/zodiac-engine/commit/65e81cb3152c9d5751f44800d649d273763ad824))

### Documentation

- Update active context with markdown formatting implementation
  ([`eccaf90`](https://github.com/gsinghjay/zodiac-engine/commit/eccaf909f793dd103688c6b00d979f27e5b29dce))

- Update progress with Gemini API integration status
  ([`b855da3`](https://github.com/gsinghjay/zodiac-engine/commit/b855da3c9db1645cb1fc3268a2c4eb8f7304e438))

- Update system patterns with markdown formatting pattern
  ([`74b575f`](https://github.com/gsinghjay/zodiac-engine/commit/74b575f9972296e4e7498d864da82e1eea3664b5))

- Update tech context with markdown library and Gemini API details
  ([`42b4a26`](https://github.com/gsinghjay/zodiac-engine/commit/42b4a2645c1d2deefbe280d4073e8614127a8264))

### Features

- Implement markdown formatting for Gemini API responses
  ([`834af50`](https://github.com/gsinghjay/zodiac-engine/commit/834af505062cc27740caa05f059a7207bb6c8607))

- Update interpretation service dependency to include LLM provider parameter
  ([`0df8836`](https://github.com/gsinghjay/zodiac-engine/commit/0df8836d5b342e4b914eb40c13f54e518c0c0a18))

- Update template to support HTML rendering from markdown
  ([`db5e9f1`](https://github.com/gsinghjay/zodiac-engine/commit/db5e9f1a138a6a79765386a955f46d9cbbdbe9b4))

- Update web routes to use run_in_threadpool for Gemini API calls
  ([`f89caf5`](https://github.com/gsinghjay/zodiac-engine/commit/f89caf5820aa02100a1d33b326c28c799e7cb88e))


## v0.5.0 (2025-05-11)

### Bug Fixes

- Add date string parsing for chart reports
  ([`932b562`](https://github.com/gsinghjay/zodiac-engine/commit/932b5621af23e73c04b22b86ce109949d30543b8))

- Centralize chart configuration defaults using ChartConfiguration schema
  ([`8d3d5a3`](https://github.com/gsinghjay/zodiac-engine/commit/8d3d5a3f42fa027176b7b48a14cb0150733001c8))

- Update API report endpoints to handle structured data
  ([`6d5983f`](https://github.com/gsinghjay/zodiac-engine/commit/6d5983fb6b1ec1bcedd0af51d0f6ac0cb74f29be))

- Update interpret methods to use report_data instead of report_text
  ([`2b71346`](https://github.com/gsinghjay/zodiac-engine/commit/2b71346080a2beef2f6219e3a2c20d37c277e468))

- Update InterpretationService to accept structured report data
  ([`e3ceacd`](https://github.com/gsinghjay/zodiac-engine/commit/e3ceacd3e2c52abdf73c534fa2565e7415f3bcdc))

- Update ReportService to return structured data for API responses
  ([`084920d`](https://github.com/gsinghjay/zodiac-engine/commit/084920d69bc34227c5dda55329689a33c0253927))

- Update web routes to work with structured report data
  ([`7bea502`](https://github.com/gsinghjay/zodiac-engine/commit/7bea50241205f370d8d26e5d04ee46a3f22f9a6c))

- Use compatibility_focus from request in synastry interpretation router
  ([`f23e27e`](https://github.com/gsinghjay/zodiac-engine/commit/f23e27e9d8b3c64e626f22fd8ef25eb95816d559))

- Use house system mapping in ReportService
  ([`a9ba5f0`](https://github.com/gsinghjay/zodiac-engine/commit/a9ba5f0b0bacffb32d199d56bf1967e83872ffab))

- **api**: Use run_in_threadpool for synchronous GeoService calls
  ([`7a41e63`](https://github.com/gsinghjay/zodiac-engine/commit/7a41e631bb04ead786fa7b6288ffaf24a24c7fb3))

- **deps**: Update GeoService dependency injection to match constructor
  ([`24bd240`](https://github.com/gsinghjay/zodiac-engine/commit/24bd240d652c958467eebf89d59b245ea16d9ef3))

- **geo**: Make GeoService methods synchronous to match requests_cache usage
  ([`df2e56e`](https://github.com/gsinghjay/zodiac-engine/commit/df2e56ed8971f8d424b4e374b77e78e03a0a52c2))

- **interpret**: Update InterpretationService to use report text format
  ([`11594a8`](https://github.com/gsinghjay/zodiac-engine/commit/11594a805a8c87659d9b699b39f632016561c7fc))

- **report**: Fix house system mapping and add ReportGenerationError
  ([`627f42b`](https://github.com/gsinghjay/zodiac-engine/commit/627f42b08c9b8fef740c5f1da7247f33b61f8f56))

- **web**: Update chart report routes to handle report text format
  ([`5100aa5`](https://github.com/gsinghjay/zodiac-engine/commit/5100aa5cf5de62cd4d1c05d24d81223f7de4bd09))

- **web**: Update location search to use run_in_threadpool and fix template variable name
  ([`19170d9`](https://github.com/gsinghjay/zodiac-engine/commit/19170d95f2d230907bbea72ef9c52e5ce9e4fe73))

### Documentation

- Update memory bank with house system mapping fixes
  ([`0bcacd0`](https://github.com/gsinghjay/zodiac-engine/commit/0bcacd0004f7f027ef6cbc24e1015c59e97719f1))

### Features

- Add compatibility_focus field to InterpretationRequest schema
  ([`030e86b`](https://github.com/gsinghjay/zodiac-engine/commit/030e86b9ca01faab7bcfffb735e1bb06a99afa68))

- Add structured report data models for interpretations
  ([`6fbfeb6`](https://github.com/gsinghjay/zodiac-engine/commit/6fbfeb6a81214ee72d6a41c529bdf512f90f29d0))

- Add type validation for report data in interpretation endpoints
  ([`0631bc6`](https://github.com/gsinghjay/zodiac-engine/commit/0631bc69f642668c7c6f2a15dbb47b0267974309))

- **report**: Enhance whole sign house explanation in template
  ([`855f39f`](https://github.com/gsinghjay/zodiac-engine/commit/855f39f99e0e41b6200f650f9ae627e837d9c733))

### Refactoring

- Optimize chart configuration handling in visualization service
  ([`6fdef5b`](https://github.com/gsinghjay/zodiac-engine/commit/6fdef5b24cf6b7ac25e099b58e433e254230578a))

- Update interpretation service to use structured report data
  ([`dc9445f`](https://github.com/gsinghjay/zodiac-engine/commit/dc9445f907d1089e5ba13c381727e66eca556218))


## v0.4.0 (2025-05-11)

### Bug Fixes

- **geo**: Update GeoService to use async methods and fix naming inconsistencies
  ([`ee563c6`](https://github.com/gsinghjay/zodiac-engine/commit/ee563c66ee36ac479ae575138357a9c57ea281c2))

- **ui**: Ensure card headers are flush with top of cards
  ([`0d7301a`](https://github.com/gsinghjay/zodiac-engine/commit/0d7301ab76afeb3325ed2095c81f02f6f7960533))

- **web**: Resolve dependency injection issue in chart download endpoint
  ([`938abf9`](https://github.com/gsinghjay/zodiac-engine/commit/938abf9a2838ed9ec3f5973ec5051921ee6ed046))

### Build System

- **deps**: Add cairosvg and Pillow dependencies for file conversion
  ([`8d78ee2`](https://github.com/gsinghjay/zodiac-engine/commit/8d78ee274e4d0e182ae4b0c1e6b7f311da4864b6))

### Chores

- Update gitignore to exclude generated chart files
  ([`f1dfd96`](https://github.com/gsinghjay/zodiac-engine/commit/f1dfd9655e51959c4b47bfe587999ef31121276e))

- Updated leftover files
  ([`d7e34b0`](https://github.com/gsinghjay/zodiac-engine/commit/d7e34b011201e7cf0489a62d020071a24f182da4))

### Documentation

- Add API structure reorganization plan to memory bank
  ([`7c51e3a`](https://github.com/gsinghjay/zodiac-engine/commit/7c51e3ae650143603bf897c51b8a449b0ea423a1))

- Update activeContext with HTMX implementation details
  ([`772b03e`](https://github.com/gsinghjay/zodiac-engine/commit/772b03e5117b332ed5a672ce32e6f401024db398))

- Update memory bank with Bootstrap migration and chart details implementation
  ([`5c4381a`](https://github.com/gsinghjay/zodiac-engine/commit/5c4381a93eaf90773d12fa433afaf2f1dbe726ea))

- Update memory bank with LLM interpretation progress
  ([`7e74058`](https://github.com/gsinghjay/zodiac-engine/commit/7e740584d8845c3690c5af43e2974929427f3d3b))

- Update progress with HTMX integration status and next steps
  ([`49b0248`](https://github.com/gsinghjay/zodiac-engine/commit/49b024857640bc119bcfc59304bb5b5e70838c15))

- Update README with LLM API configuration instructions
  ([`aca8ae0`](https://github.com/gsinghjay/zodiac-engine/commit/aca8ae0c2ab0430819e13633cb4998621405f341))

- Update techContext with API structure reorganization plan
  ([`344846d`](https://github.com/gsinghjay/zodiac-engine/commit/344846d801e9c51a365b5cfea6b9570bb1475bda))

### Features

- Add interpretation and report UI to chart details page
  ([`2531256`](https://github.com/gsinghjay/zodiac-engine/commit/25312566c9de22a1c9cbfcac914df906dd72f937))

- Add interpretations router to chart routers
  ([`0bd06b2`](https://github.com/gsinghjay/zodiac-engine/commit/0bd06b23c99d42e45c18e2c869b837feaee95f02))

- Add InterpretationService dependency injection
  ([`8b50612`](https://github.com/gsinghjay/zodiac-engine/commit/8b506120cabedad1bb088da425adff505d554e8a))

- Add LLM API settings configuration
  ([`e1fe81d`](https://github.com/gsinghjay/zodiac-engine/commit/e1fe81df457a79622079c0e0c8802f00040b8930))

- Add web routes for interpretation and report generation
  ([`e7f9fb6`](https://github.com/gsinghjay/zodiac-engine/commit/e7f9fb69e420f20446acc1b0adc22ecb886304e7))

- Create chart interpretation API endpoints
  ([`2f4e7dc`](https://github.com/gsinghjay/zodiac-engine/commit/2f4e7dcc64cf5fa3d03f0a5c4dbe2806e77d0196))

- Create chart report API endpoints
  ([`710787b`](https://github.com/gsinghjay/zodiac-engine/commit/710787bedac8a593bf72a71aab8980971eb986b7))

- Create interpretation display template fragment
  ([`0e7ac23`](https://github.com/gsinghjay/zodiac-engine/commit/0e7ac23971ea7cea63ae12d4fae626e7ee5d931c))

- Create interpretation service with LLM integration structure
  ([`89fa8fd`](https://github.com/gsinghjay/zodiac-engine/commit/89fa8fd4c1f2af7ee9608df962b1b3ecc3595fd2))

- Create report display template fragment
  ([`ba65673`](https://github.com/gsinghjay/zodiac-engine/commit/ba656735beaa585698a157029a13c84cc9b73bd9))

- Create schemas for report and interpretation data
  ([`57322c9`](https://github.com/gsinghjay/zodiac-engine/commit/57322c97a34675eb748d1fd27b5a9427142a5dc9))

- Implement report generation service with Kerykeion integration
  ([`8f69663`](https://github.com/gsinghjay/zodiac-engine/commit/8f6966345538292f3452a5a73e2a825f397657bc))

- **cache**: Implement in-memory chart data cache for persistence between requests
  ([`c284cf9`](https://github.com/gsinghjay/zodiac-engine/commit/c284cf9d7e9f0b34d863ecb88fd9d82f8bca6356))

- **core**: Add dependency injection for FileConversionService
  ([`f23dda3`](https://github.com/gsinghjay/zodiac-engine/commit/f23dda3b2340b9dec9c4bee0a151aa7473951c79))

- **core**: Add FileConversionError to exception handling
  ([`72c6f70`](https://github.com/gsinghjay/zodiac-engine/commit/72c6f70531ceadd3f97d23f7f8022590557352d3))

- **core**: Add SVG CSS variable preprocessing utility functions
  ([`e6b7be7`](https://github.com/gsinghjay/zodiac-engine/commit/e6b7be7d84a78015efa340d2f2d5a0fe18aa3c80))

- **routes**: Update web routes to handle chart details page and implement redirect flow
  ([`9aaacc5`](https://github.com/gsinghjay/zodiac-engine/commit/9aaacc5d0ef7f6638cf5728af13777708532d7a3))

- **services**: Implement FileConversionService for SVG to PNG/PDF/JPEG conversion
  ([`6a65ab8`](https://github.com/gsinghjay/zodiac-engine/commit/6a65ab8c9e0f966d835e1e3131edd78f70743969))

- **ui**: Add JPEG download option and DPI guidance to chart details page
  ([`271ab69`](https://github.com/gsinghjay/zodiac-engine/commit/271ab69eab04f1df90b13c29bc689826a96d5c62))

- **ui**: Add reusable template fragments for component consistency
  ([`6e65fd7`](https://github.com/gsinghjay/zodiac-engine/commit/6e65fd70a2f962925140eaabcfe7168e8c98b904))

- **ui**: Create dedicated chart details page with two-column layout
  ([`dec625d`](https://github.com/gsinghjay/zodiac-engine/commit/dec625d990a106e65d7e1fbfa0599c52e605e6bd))

- **ui**: Integrate Bootstrap CSS and JS into layout template
  ([`45e3624`](https://github.com/gsinghjay/zodiac-engine/commit/45e3624ecae75cb51d7918c634409d2d3c8a8b1e))

### Refactoring

- Consolidate router structure to follow FastAPI best practices
  ([`7c11179`](https://github.com/gsinghjay/zodiac-engine/commit/7c11179d52ad25741ebfd04a8be41315ffb2c026))

- **css**: Simplify custom styles to use Bootstrap with minimal overrides
  ([`ffe0eac`](https://github.com/gsinghjay/zodiac-engine/commit/ffe0eac76d341f25d53373b058695bfcb5740382))

- **ui**: Update home page forms with Bootstrap components and classes
  ([`8028064`](https://github.com/gsinghjay/zodiac-engine/commit/8028064a4f809d0ddd49aa635e9dcca1b370d16e))

### Testing

- **scripts**: Add test scripts for SVG preprocessing and file conversion
  ([`a348667`](https://github.com/gsinghjay/zodiac-engine/commit/a348667d162e2c457e07a771cfc3c14d8dda4c13))


## v0.3.0 (2025-04-29)

### Bug Fixes

- Enable online GeoNames lookup when username is present
  ([`98dd793`](https://github.com/gsinghjay/zodiac-engine/commit/98dd7933237ca5f436d8ba60018296ca451c8b1d))

- Remove non-existent static router import
  ([`cc5f438`](https://github.com/gsinghjay/zodiac-engine/commit/cc5f438372611e3b331907b4e78933dfe6096030))

- Resolve root path redirect loop
  ([`a027b00`](https://github.com/gsinghjay/zodiac-engine/commit/a027b0049a51e5cb932eba501aba6ed003bc54e4))

### Chores

- Add geopy dependency
  ([`3ccf336`](https://github.com/gsinghjay/zodiac-engine/commit/3ccf336b25ee9007ec265b7ba89a9104f066f33e))

- Improve logging for SVG directory creation
  ([`2f92349`](https://github.com/gsinghjay/zodiac-engine/commit/2f923490006c91550f5b72eb1d973d4b910d610d))

### Documentation

- Add README for API test scripts
  ([`594271b`](https://github.com/gsinghjay/zodiac-engine/commit/594271bde91f4fe0a5ac6559b369f99d1615e0a9))

- Update memory bank with GeoNames integration and debugging
  ([`904472d`](https://github.com/gsinghjay/zodiac-engine/commit/904472daca100606a57da4357d91cb6159a79c49))

- Update README (update based on actual changes)
  ([`66328ef`](https://github.com/gsinghjay/zodiac-engine/commit/66328efaeddc44c5458c6a59d822745cd9b53d2b))

### Features

- Add dependency provider for GeoService
  ([`c99a45f`](https://github.com/gsinghjay/zodiac-engine/commit/c99a45fce6d9186a13cc072e4d9013e820eb93a6))

- Add geo API endpoint for city search
  ([`ab13fe3`](https://github.com/gsinghjay/zodiac-engine/commit/ab13fe33b394ace7383f1bdf6825e4fd019d5efb))

- Add Jinja2 templates for web interface
  ([`ba4e355`](https://github.com/gsinghjay/zodiac-engine/commit/ba4e355af0f2a9c3f37013e0a3d9b038f80ed595))

- Add script to test Vedic chart generation via API
  ([`22dc71d`](https://github.com/gsinghjay/zodiac-engine/commit/22dc71d13cdfee6a6fb19b8d4fd4167e084695e1))

- Add script to test Western chart generation via API
  ([`0a277c1`](https://github.com/gsinghjay/zodiac-engine/commit/0a277c1e24e2e47c64f7e189f70134721a9ff798))

- Add styles for web interface and location search
  ([`4bf964c`](https://github.com/gsinghjay/zodiac-engine/commit/4bf964ce064e219ca347b05dcde300d4b19013cb))

- Add web routes for home page and chart generation
  ([`b704c25`](https://github.com/gsinghjay/zodiac-engine/commit/b704c25117d7aacb83b29f2f81af6c6e84dd7d79))

- Implement GeoService for GeoNames lookup
  ([`28b9d47`](https://github.com/gsinghjay/zodiac-engine/commit/28b9d47c52f6456112c9a8398cf1132210595056))

- Include geo router in API v1
  ([`8707097`](https://github.com/gsinghjay/zodiac-engine/commit/87070977455d50c2f626c8a37c593f422a483f2f))


## v0.2.0 (2025-04-28)

### Bug Fixes

- Add sample.svg file for test environment
  ([`d5169df`](https://github.com/gsinghjay/zodiac-engine/commit/d5169df7bdb377f294311117536786eef6912745))

- Remove @staticmethod from synastry chart method to fix self reference
  ([`8160f0c`](https://github.com/gsinghjay/zodiac-engine/commit/8160f0c7413403080c17bc0b49f2571aad6b10d6))

- Update CORS middleware to use allowed_origins_list property
  ([`148494a`](https://github.com/gsinghjay/zodiac-engine/commit/148494afacd38e5bce961a7e7e6c4dba290f58f8))

- Update Settings class to use Pydantic v2 and handle ALLOWED_ORIGINS properly
  ([`74a632f`](https://github.com/gsinghjay/zodiac-engine/commit/74a632f170e6c3c929c78547f5e4e73832169e2f))

### Chores

- Add sample SVG for test fixtures
  ([`d52d04a`](https://github.com/gsinghjay/zodiac-engine/commit/d52d04a58319f76bcc2b0671849ddf983dcac8ca))

- Deleted test svg files
  ([`6d74644`](https://github.com/gsinghjay/zodiac-engine/commit/6d74644f7aec6188b2ee913185813e1cc29ba196))

- Ignore generated SVG files
  ([`e59f79d`](https://github.com/gsinghjay/zodiac-engine/commit/e59f79da05123e93d70ab8662aa37422184d0a1b))

- Remove test-generated SVG files
  ([`c69bac2`](https://github.com/gsinghjay/zodiac-engine/commit/c69bac2f12bb3902e6e86d499ba2009a72d5915d))

- Update dependencies with explicit version constraints
  ([`c920ca2`](https://github.com/gsinghjay/zodiac-engine/commit/c920ca2a49d88090b49397b284b2253426abc4e4))

### Documentation

- Update active context after API router migration
  ([`9b88b28`](https://github.com/gsinghjay/zodiac-engine/commit/9b88b28d76afd17cb438b98e6b307b313db0b306))

- Update Cursor rules with FastAPI best practices
  ([`f94acbd`](https://github.com/gsinghjay/zodiac-engine/commit/f94acbd5e5c485ed39424a07055981d354156679))

- Update memory bank with FastAPI best practices implementation
  ([`b055e13`](https://github.com/gsinghjay/zodiac-engine/commit/b055e13096cf670f54b47c0603605b5511fc1095))

- Update memory bank with FastAPI best practices implementation status
  ([`3bb1e8c`](https://github.com/gsinghjay/zodiac-engine/commit/3bb1e8c2d2566cd58effdbd66d60f22207bf86e0))

- Update memory bank with test improvements
  ([`114ee91`](https://github.com/gsinghjay/zodiac-engine/commit/114ee918cfb46fcf7ff221730f046ff5d1887022))

- Update progress after API router migration
  ([`44d445c`](https://github.com/gsinghjay/zodiac-engine/commit/44d445c9201b740393d679076d30b8e90a8f3716))

- Update README with environment variable documentation
  ([`1e4afcc`](https://github.com/gsinghjay/zodiac-engine/commit/1e4afcc4e663eef014de1a5990cf653f76fb1c22))

- Update README with environment variables docs and testing instructions
  ([`abc0b1d`](https://github.com/gsinghjay/zodiac-engine/commit/abc0b1d3d8b4b0c34f007752d6a471c125fe0748))

- **memory**: Update memory bank with natal chart expansion plan
  ([`f0f3def`](https://github.com/gsinghjay/zodiac-engine/commit/f0f3defe8433a06bf15e63b2101348e8ff56979c))

### Features

- Add factory functions for service dependencies
  ([`4dab3a3`](https://github.com/gsinghjay/zodiac-engine/commit/4dab3a38f253e34e6d21e13223b8fb4bad2f1824))

- **core**: Update dependency injection and error handling
  ([`756b5b3`](https://github.com/gsinghjay/zodiac-engine/commit/756b5b391660e1f68d048d7467590c00edf31782))

- **schemas**: Migrate to Pydantic v2 syntax
  ([`0f0f0fb`](https://github.com/gsinghjay/zodiac-engine/commit/0f0f0fbdba054919a689cca3d3cdac2cceb42969))

### Refactoring

- Convert static methods to instance methods with proper DI
  ([`ee85010`](https://github.com/gsinghjay/zodiac-engine/commit/ee8501044c63fbc92266a2407549052876e0e6fb))

- Migrate API structure from endpoints to routers directory
  ([`2afd4b4`](https://github.com/gsinghjay/zodiac-engine/commit/2afd4b42407ad00ca2856d5ddfdbaa396350bded))

- Update API v1 imports to use routers instead of endpoints
  ([`adf0bb1`](https://github.com/gsinghjay/zodiac-engine/commit/adf0bb1ae901e1f43d79bf1d1d1c89e187a4e6ac))

- Update chart visualization endpoints to use service DI
  ([`a85f79a`](https://github.com/gsinghjay/zodiac-engine/commit/a85f79ac750c00a0cc8a1ea17e4e4019d548091a))

- Update chart visualization schemas to Pydantic v2 syntax
  ([`3d81c4d`](https://github.com/gsinghjay/zodiac-engine/commit/3d81c4dbfbe69831b1edbf505ee6abed61646cdc))

- Update natal chart endpoints to use service DI
  ([`02550fe`](https://github.com/gsinghjay/zodiac-engine/commit/02550fe2710927bfbc5449ba5ff7e0347a5531b3))

- Update natal chart schemas to Pydantic v2 syntax
  ([`6363c4f`](https://github.com/gsinghjay/zodiac-engine/commit/6363c4f60a58c1ffd0a091915163d69782c9415f))

- **api**: Update routers to use dependency injection
  ([`11e8d07`](https://github.com/gsinghjay/zodiac-engine/commit/11e8d07f1d95aebcb1febaa81f34ab55a4e054c8))

- **services**: Convert static methods to instance methods with DI
  ([`715df6d`](https://github.com/gsinghjay/zodiac-engine/commit/715df6d1bf8e74f186f5fe46c3eaee4fcf73d7b6))

### Testing

- Update tests to follow FastAPI best practices
  ([`a9f89cd`](https://github.com/gsinghjay/zodiac-engine/commit/a9f89cd5abf97292f3af0520ac5497aa5e6ebfdf))

- Update tests to use FastAPI best practices
  ([`1861b42`](https://github.com/gsinghjay/zodiac-engine/commit/1861b42aa9808428a060fd9a0d1b95fc123d3fae))


## v0.1.0 (2025-04-01)

### Chores

- Add cache directory to gitignore
  ([`3899142`](https://github.com/gsinghjay/zodiac-engine/commit/389914254dad77f37478b103ab411a7343647704))

- Add example chart SVG outputs
  ([`2efcc20`](https://github.com/gsinghjay/zodiac-engine/commit/2efcc20d90b1d9a5037e6cab6b14167e7151ad46))

- Initialize project configuration
  ([`22d84b0`](https://github.com/gsinghjay/zodiac-engine/commit/22d84b06efb26394784d7f625fb364f6dfd883f3))

### Continuous Integration

- Added semantic release
  ([`481ebc3`](https://github.com/gsinghjay/zodiac-engine/commit/481ebc3c173f9b24aa8f1f8181ec60d8b5400072))

### Documentation

- Add comprehensive README and update gitignore
  ([`3311358`](https://github.com/gsinghjay/zodiac-engine/commit/33113587d254554c40bb917567cec52edca01190))

- Update README with new chart visualization features
  ([`868d11c`](https://github.com/gsinghjay/zodiac-engine/commit/868d11c3e5389c636887b20c10f3c46d23942364))

### Features

- Add core services and data schemas
  ([`7d6476a`](https://github.com/gsinghjay/zodiac-engine/commit/7d6476a0d9033461bcd08a6ce71e0fbbefaace42))

- Add dependency injection for application settings
  ([`75547ab`](https://github.com/gsinghjay/zodiac-engine/commit/75547ab37add5f896a180759379f52e64bad19b4))

- Add house system configuration to natal chart endpoint
  ([`9e61f33`](https://github.com/gsinghjay/zodiac-engine/commit/9e61f334c81f0cf569c5d9b451eca80647ac6730))

- Add house system schema and update natal chart response
  ([`c4fce46`](https://github.com/gsinghjay/zodiac-engine/commit/c4fce46fad9e6fc3117d00e78d482a98bb251b9a))

- Add static file serving capability for chart images
  ([`ee51997`](https://github.com/gsinghjay/zodiac-engine/commit/ee519977c5de46b5f867e9f415270a8e2a8f96d8))

- Add support for additional celestial points in natal chart
  ([`557b2d2`](https://github.com/gsinghjay/zodiac-engine/commit/557b2d2ffc5bd9c01ab8ebc9444a9fa6bf5b9aa2))

- Configure main application with error handling and documentation
  ([`e6dccab`](https://github.com/gsinghjay/zodiac-engine/commit/e6dccab4ec1710a0dd389d206b0a1495f70943cb))

- Enhance chart visualization endpoints with additional options
  ([`b156346`](https://github.com/gsinghjay/zodiac-engine/commit/b1563464fa0ae758bd6921f797b92fbf9a44dfd7))

- Enhance chart visualization schemas with additional configuration options
  ([`3d24c58`](https://github.com/gsinghjay/zodiac-engine/commit/3d24c58bfc1f40fcff56c0cc269e9710c143bc98))

- Implement API structure with versioned endpoints
  ([`73cbdc1`](https://github.com/gsinghjay/zodiac-engine/commit/73cbdc170d6cc556bf6b2e4dfcea448939d53ad7))

- Implement chart visualization using Kerykeion SVG
  ([`b75a053`](https://github.com/gsinghjay/zodiac-engine/commit/b75a053ac6ba4ba77946a56c4e1ff60a2d8847c0))

- Implement extended visualization options for natal charts
  ([`f1794ae`](https://github.com/gsinghjay/zodiac-engine/commit/f1794aec806b9b2cc61015f7ebb18c889df37f87))

### Refactoring

- Move static files handling from router to FastAPI static mounting
  ([`2a36e97`](https://github.com/gsinghjay/zodiac-engine/commit/2a36e970e4d18534d6b3cf63541baeca1586808e))

### Testing

- Add comprehensive chart configuration tests
  ([`3b3a60b`](https://github.com/gsinghjay/zodiac-engine/commit/3b3a60be65cf2fc3a600595163065af858f37df3))

- Add comprehensive test suite for API endpoints
  ([`a9c4332`](https://github.com/gsinghjay/zodiac-engine/commit/a9c4332d03ceb16c710602c5a517fe4468714f8a))

- Add comprehensive tests for natal chart variations
  ([`6bfbbf2`](https://github.com/gsinghjay/zodiac-engine/commit/6bfbbf246682e7f8628fb80a9e5db4a9576e6986))

- Add tests for celestial points, aspects and house systems
  ([`3cc96d9`](https://github.com/gsinghjay/zodiac-engine/commit/3cc96d9fd8d9e4dc9e0cc6c586f86c374fa0ab02))
