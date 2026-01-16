---
goal: Comprehensive Refactoring of AI Browser Agent Architecture
version: 1.0
date_created: 2026-01-16
last_updated: 2026-01-16
owner: Development Team
status: 'Planned'
tags: [refactor, architecture, testing, dependency-management, code-quality]
---

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This implementation plan outlines a comprehensive refactoring of the AI Browser Agent project to improve code quality, maintainability, testability, and production readiness. The refactoring addresses technical debt, improves dependency management, enhances error handling, expands test coverage, and implements better configuration management practices.

## 1. Requirements & Constraints

### Requirements

- **REQ-001**: Maintain backward compatibility with existing API interfaces where possible
- **REQ-002**: All code must use async/await patterns consistently for I/O operations
- **REQ-003**: Achieve minimum 80% test coverage across all modules
- **REQ-004**: All modules must have comprehensive docstrings and type hints
- **REQ-005**: Configuration must be environment-aware (dev, test, prod)
- **REQ-006**: Dependencies must be properly versioned and organized
- **REQ-007**: Error handling must include proper logging and graceful degradation
- **REQ-008**: All external API calls must include retry logic and circuit breakers
- **REQ-009**: Browser automation must support headless and headed modes
- **REQ-010**: LLM processing must support multiple model providers (OpenAI, Anthropic, etc.)

### Security Requirements

- **SEC-001**: API keys must never be hardcoded or committed to version control
- **SEC-002**: Environment variables must be validated on application startup
- **SEC-003**: HTML content must be sanitized before processing
- **SEC-004**: Rate limiting must be implemented for external API calls
- **SEC-005**: Sensitive data must not be logged

### Performance Constraints

- **CON-001**: HTML truncation must preserve semantic structure and not exceed token limits
- **CON-002**: Browser initialization overhead must be minimized through connection pooling
- **CON-003**: Memory usage must be bounded for large HTML documents
- **CON-004**: Concurrent scraping operations must be limited to prevent resource exhaustion

### Guidelines

- **GUD-001**: Follow Python PEP 8 style guidelines consistently
- **GUD-002**: Use Pydantic for all data validation and serialization
- **GUD-003**: Prefer composition over inheritance
- **GUD-004**: Keep functions focused on single responsibilities
- **GUD-005**: Use context managers for resource management
- **GUD-006**: Document all public APIs with examples

### Patterns to Follow

- **PAT-001**: Use dependency injection for external dependencies (API clients, browser instances)
- **PAT-002**: Implement repository pattern for data access
- **PAT-003**: Use factory pattern for creating configured instances
- **PAT-004**: Apply strategy pattern for multiple LLM providers
- **PAT-005**: Use observer pattern for progress tracking and callbacks

## 2. Implementation Steps

### Implementation Phase 1: Project Structure & Dependency Management

- GOAL-001: Reorganize project structure for better modularity and establish proper dependency management

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Completed | Date |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| TASK-001 | Create `setup.py` or `pyproject.toml` for package distribution with metadata (name, version, author, description, dependencies). Include entry points for CLI usage. Use `pyproject.toml` following PEP 621 standards with build-system section specifying `setuptools>=61.0`. Define package dependencies in `[project]` section and development dependencies in `[project.optional-dependencies]`. Include classifiers for Python versions and project maturity.                                                                                                      |           |      |
| TASK-002 | Split `requirements.txt` into separate files: `requirements.txt` (production), `requirements-dev.txt` (development tools: pytest, pytest-asyncio, pytest-cov, black, flake8, mypy, isort), `requirements-test.txt` (testing only). Pin exact versions for production dependencies. In `requirements-dev.txt`, include `-r requirements.txt` to inherit production dependencies. Add version ranges where appropriate for flexibility.                                                                                                                                  |           |      |
| TASK-003 | Create `.python-version` file specifying Python 3.8+ requirement. Add section to README.md documenting supported Python versions and how to install dependencies using `pip install -r requirements.txt` and `pip install -r requirements-dev.txt` for development.                                                                                                                                                                                                                                                                                                  |           |      |
| TASK-004 | Reorganize `src/` directory structure: Create subdirectories `src/ai_browser_agent/` with `__init__.py`, `src/ai_browser_agent/scrapers/` for web scraping modules, `src/ai_browser_agent/processors/` for LLM processing, `src/ai_browser_agent/services/` for orchestration services, `src/ai_browser_agent/models/` for data models, `src/ai_browser_agent/config/` for configuration, `src/ai_browser_agent/utils/` for helper utilities. Move existing modules to appropriate subdirectories and update all import statements throughout the codebase. |           |      |
| TASK-005 | Create `src/ai_browser_agent/__init__.py` with explicit exports of main classes: `WebScraperAgent`, `LLMProcessor`, `ScrapingService`, and main models. Include `__version__` attribute. Add `__all__` list to control public API. Import and re-export key functions and classes to provide clean top-level API.                                                                                                                                                                                                                                                    |           |      |
| TASK-006 | Add `Makefile` or `justfile` for common development tasks: `install` (install dependencies), `install-dev` (install dev dependencies), `test` (run tests), `lint` (run linters), `format` (format code), `type-check` (run mypy), `clean` (remove cache files), `browser-install` (install Playwright browsers). Each task should have clear error handling and output.                                                                                                                                                                                            |           |      |

### Implementation Phase 2: Configuration Management Enhancement

- GOAL-002: Implement robust configuration management with environment-specific settings and validation

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Completed | Date |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| TASK-007 | Create `src/ai_browser_agent/config/settings.py` using Pydantic Settings for configuration management. Define `Settings` class with fields: `openai_api_key: SecretStr`, `default_model: str`, `max_html_tokens: int`, `browser_headless: bool`, `log_level: str`, `page_timeout: int`, `retry_attempts: int`, `retry_delay: float`, etc. Use Pydantic Field with descriptions and validation. Add `model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)` to enable automatic .env loading. Include validators for API keys, token limits, and timeout values using `@field_validator`. |           |      |
| TASK-008 | Create `src/ai_browser_agent/config/environments.py` with environment-specific configurations. Define `Environment` enum with values: `DEVELOPMENT`, `TESTING`, `PRODUCTION`. Create configuration classes: `DevelopmentConfig(Settings)`, `TestingConfig(Settings)`, `ProductionConfig(Settings)`. Override settings as needed (e.g., `browser_headless=False` for dev, strict timeouts for prod). Implement factory function `get_settings(env: Environment) -> Settings` that returns appropriate config instance.                                                                                                                            |           |      |
| TASK-009 | Add `.env.example` file with all required environment variables documented: `OPENAI_API_KEY=your_key_here`, `MULTION_API_KEY=your_key_here`, `ENVIRONMENT=development`, `LOG_LEVEL=INFO`, `BROWSER_HEADLESS=true`, etc. Include comments explaining each variable's purpose and acceptable values.                                                                                                                                                                                                                                                                                                                                       |           |      |
| TASK-010 | Update existing `src/ai_browser_agent/config/__init__.py` to expose new settings system. Import and instantiate settings: `from .settings import Settings; settings = Settings()`. Re-export commonly used configuration values for backward compatibility: `TARGET_URL = settings.target_url`, `DEFAULT_MODEL = settings.default_model`, etc. Add deprecation warnings for direct constant imports.                                                                                                                                                                                                                                      |           |      |
| TASK-011 | Create configuration validation function in `settings.py`: `validate_config(settings: Settings) -> bool` that checks for required API keys, validates token limits are within bounds, ensures timeout values are positive, validates model names against supported models list. This function should be called on application startup in `main.py`. Raise descriptive `ConfigurationError` exception with clear instructions if validation fails.                                                                                                                                                                                            |           |      |

### Implementation Phase 3: Error Handling & Resilience

- GOAL-003: Implement comprehensive error handling, retry logic, and resilience patterns throughout the application

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Completed | Date |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ---- |
| TASK-012 | Create `src/ai_browser_agent/exceptions.py` module with custom exception hierarchy: `BrowserAgentError(Exception)` as base, `ScrapingError(BrowserAgentError)` for scraping failures, `ProcessingError(BrowserAgentError)` for LLM failures, `ConfigurationError(BrowserAgentError)` for config issues, `BrowserInitError(ScrapingError)` for browser setup failures, `NavigationError(ScrapingError)` for page navigation issues, `TokenLimitError(ProcessingError)` for token limit issues, `APIError(ProcessingError)` for API call failures. Each exception should accept `message: str`, `original_error: Optional[Exception]`, and `context: Optional[Dict[str, Any]]`. | --------- | ---- |
| TASK-013 | Create `src/ai_browser_agent/utils/retry.py` with decorator `@retry_with_backoff` that accepts parameters: `max_attempts: int`, `initial_delay: float`, `backoff_factor: float`, `exceptions: Tuple[Type[Exception], ...]`. Implement exponential backoff with jitter. Log each retry attempt with attempt number and delay. After max attempts exceeded, raise the last exception with added context about retry attempts. Use `functools.wraps` to preserve function metadata.                                                                                                                                                                                                       |           |      |
| TASK-014 | Apply retry decorator to critical operations in `web_scraper.py`: `scrape_content()` should retry on `PlaywrightError` with 3 attempts, 2s initial delay, 2x backoff. `take_screenshot()` should retry on transient errors with 2 attempts. Update function signatures to include type hints for exceptions that may be raised. Add logging before retry attempts: `logger.warning(f"Retrying {func.__name__} after {delay}s (attempt {attempt}/{max_attempts})")`.                                                                                                                                                                                                                  |           |      |
| TASK-015 | Apply retry decorator to LLM API calls in `llm_processor.py`: `process_html_to_structured_data()` should retry on rate limit errors and transient API failures with 4 attempts, 1s initial delay, 2x backoff. Implement specific handling for `RateLimitError` to wait longer. Add circuit breaker pattern: after 5 consecutive failures, temporarily disable API calls for 60 seconds, then allow one test call. Track circuit state in class variable. Log circuit state changes.                                                                                                                                                                                                         |           |      |
| TASK-016 | Add graceful error handling to `scraping_service.py`: Wrap operations in try-except blocks with specific exception handling for `ScrapingError`, `ProcessingError`, `ConfigurationError`. On error, log full stack trace at ERROR level, clean up resources (close browser), return structured error response instead of None: `ErrorResult(error_type: str, message: str, details: Optional[Dict])`. Add `success: bool` field to return type. Update return type annotations to use `Union[SuccessResult, ErrorResult]`.                                                                                                                                              |           |      |

### Implementation Phase 4: Testing Infrastructure

- GOAL-004: Establish comprehensive testing infrastructure with unit tests, integration tests, and mocking utilities

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Completed | Date |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| TASK-017 | Create `tests/conftest.py` with pytest fixtures: `mock_browser` (yields mocked Playwright browser with page), `mock_openai_client` (yields mocked AsyncOpenAI with parse response), `sample_html` (returns test HTML content), `sample_screenshot` (returns bytes of test PNG), `test_settings` (returns Settings with test configuration), `event_loop` (configures pytest-asyncio event loop). Each fixture should have proper scope (`function`, `module`, or `session`). Add docstrings explaining fixture purpose and usage.                                                                                                                 |           |      |
| TASK-018 | Create unit tests in `tests/unit/test_web_scraper.py`: Test `WebScraperAgent.init_browser()` successfully initializes, test context manager properly cleans up resources, test `scrape_content()` with mocked page returns HTML, test `scrape_content()` raises `ScrapingError` on navigation failure, test screenshot methods return expected data types, test retry logic triggers on failures, test browser args are properly applied. Use `pytest.mark.asyncio` for async tests. Mock Playwright using `unittest.mock.AsyncMock`. Verify logger calls using mock assertions. Aim for >90% coverage of `web_scraper.py`.                                |           |      |
| TASK-019 | Create unit tests in `tests/unit/test_llm_processor.py`: Test token counting accuracy with known inputs, test HTML truncation preserves structure and stays within limits, test `process_html_to_structured_data()` with mocked API returns expected model, test handling of API errors and rate limits, test retry logic for transient failures, test circuit breaker opens after consecutive failures, test generic type handling with different Pydantic models, test validation of malformed responses. Mock `AsyncOpenAI` client. Verify structured output parsing. Test with multiple model types. Aim for >90% coverage of `llm_processor.py`. |           |      |
| TASK-020 | Create unit tests in `tests/unit/test_scraping_service.py`: Test `scrape_and_process()` orchestrates scraper and processor correctly, test error handling returns structured error responses, test resource cleanup on failures, test backward compatibility with legacy function, test successful flow returns correct tuple structure, test screenshot is captured before processing. Mock both `WebScraperAgent` and `LLMProcessor`. Use fixtures from `conftest.py`. Verify integration between components. Aim for >85% coverage of `scraping_service.py`.                                                                                         |           |      |
| TASK-021 | Create integration tests in `tests/integration/test_end_to_end.py`: Test complete flow from URL to structured data with real browser but mocked LLM, test with sample HTML file instead of network call, test error propagation through the stack, test configuration changes affect behavior, test multiple concurrent scraping operations, test memory cleanup after operations. Use `pytest-xdist` for parallel test execution. Mark slow tests with `@pytest.mark.slow`. These tests should use real Playwright but mock OpenAI API.                                                                                                           |           |      |
| TASK-022 | Configure `pytest.ini` with settings: `asyncio_mode = auto`, markers for `unit`, `integration`, `slow`, `requires_browser`, test paths, coverage options (`--cov=src/ai_browser_agent`, `--cov-report=html`, `--cov-report=term-missing`, `--cov-fail-under=80`). Add logging configuration for tests. Configure pytest-asyncio default fixture loop scope. Add timeout settings for tests using `pytest-timeout`.                                                                                                                                                                                                                                  |           |      |

### Implementation Phase 5: Code Quality & Documentation

- GOAL-005: Improve code quality through linting, formatting, type checking, and comprehensive documentation

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Completed | Date |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ---- |
| TASK-023 | Add `pyproject.toml` configuration sections for tools: `[tool.black]` with `line-length = 100`, `target-version = ['py38', 'py39', 'py310']`, `[tool.isort]` with `profile = "black"`, `line_length = 100`, `[tool.mypy]` with `python_version = "3.8"`, `strict = true`, `warn_return_any = true`, `warn_unused_configs = true`, `disallow_untyped_defs = true`, `[tool.pytest.ini_options]` with test configurations. Add `[tool.coverage.run]` with `source = ["src"]`, `omit = ["*/tests/*", "*/__pycache__/*"]`, and `[tool.coverage.report]` with `exclude_lines` for pragmas and abstract methods. |           |      |
| TASK-024 | Create `.flake8` configuration file with settings: `max-line-length = 100`, `extend-ignore = E203, W503` (for Black compatibility), `exclude = .git, __pycache__, .venv, .eggs, *.egg, build, dist`, `max-complexity = 10`. Add per-file ignores if needed for generated code or migrations.                                                                                                                                                                                                                                                                                                              |           |      |
| TASK-025 | Run `black` on entire codebase: `black src/ tests/`. Verify all files are formatted consistently. Commit formatting changes separately from logic changes.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |           |      |
| TASK-026 | Run `isort` on entire codebase: `isort src/ tests/`. Verify imports are sorted correctly: stdlib, third-party, first-party. Commit import sorting changes.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |           |      |
| TASK-027 | Run `mypy` on codebase: `mypy src/`. Fix all type errors: Add missing type hints to function parameters and return types, add type hints to class attributes, use `typing` module for complex types (`Optional`, `Union`, `List`, `Dict`, `Tuple`, `TypeVar`), resolve any type incompatibilities. Update function signatures in `web_scraper.py`, `llm_processor.py`, `scraping_service.py`, `helpers.py` to be fully typed. Add `# type: ignore` comments only where absolutely necessary with explanatory comment.                                                                                          |           |      |
| TASK-028 | Enhance docstrings across all modules using Google-style docstring format: Add module-level docstrings describing purpose and main exports, add class docstrings with attributes section, add method/function docstrings with Args, Returns, Raises, Examples sections. Update `web_scraper.py`, `llm_processor.py`, `scraping_service.py`, `models.py`, `config.py`, `helpers.py`. Include usage examples in complex functions. Document all exceptions that may be raised.                                                                                                                                 |           |      |
| TASK-029 | Create `CONTRIBUTING.md` with development guidelines: How to set up development environment, how to run tests, code style requirements (Black, isort, flake8, mypy), how to submit pull requests, commit message conventions, code review process. Include commands for common tasks: `make install-dev`, `make test`, `make lint`, `make format`, `make type-check`. Add section on adding new features and writing tests.                                                                                                                                                                                    |           |      |

### Implementation Phase 6: Advanced Features & Extensibility

- GOAL-006: Add advanced features including multi-provider support, browser pooling, and plugin architecture

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Completed | Date |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| TASK-030 | Create `src/ai_browser_agent/processors/base.py` with abstract `BaseLLMProcessor(ABC)` class defining interface: `@abstractmethod async def process(html: str, instructions: str, model: Type[T]) -> T`. Include methods: `count_tokens()`, `truncate_content()`, `validate_response()`. This will enable multiple LLM provider implementations.                                                                                                                                                                                                                                                                                                                                                    |           |      |
| TASK-031 | Refactor existing `LLMProcessor` to extend `BaseLLMProcessor` and rename to `OpenAIProcessor`. Move to `src/ai_browser_agent/processors/openai.py`. Ensure it implements all abstract methods from base class. Keep existing functionality intact.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |           |      |
| TASK-032 | Create `src/ai_browser_agent/processors/anthropic.py` with `AnthropicProcessor(BaseLLMProcessor)` class. Implement using Anthropic's API client with similar structured output approach. Handle token counting using Anthropic's tokenizer. Implement retry logic and error handling specific to Anthropic API. Use `instructor` library for structured outputs from Claude. Configure with API key from settings. Support Claude 3.5 Sonnet and other models.                                                                                                                                                                                                                                          |           |      |
| TASK-033 | Create processor factory in `src/ai_browser_agent/processors/factory.py`: `ProcessorFactory` class with `create_processor(provider: str, **kwargs) -> BaseLLMProcessor` method. Support providers: `"openai"`, `"anthropic"`. Load configuration from settings. Register processors using dictionary mapping. Add method to list available providers. Implement singleton pattern to reuse processor instances. Add validation for provider names and required configuration.                                                                                                                                                                                                                            |           |      |
| TASK-034 | Create browser pool in `src/ai_browser_agent/scrapers/browser_pool.py`: `BrowserPool` class managing multiple browser instances. Implement `async def acquire() -> WebScraperAgent` to get browser from pool, `async def release(browser: WebScraperAgent)` to return to pool, `async def close_all()` to cleanup. Use `asyncio.Queue` for managing available browsers. Set configurable pool size (default 3). Implement health checks for browsers. Add metrics: total browsers, active browsers, wait time. Use context manager protocol for automatic acquire/release.                                                                                                                           |           |      |
| TASK-035 | Create plugin system in `src/ai_browser_agent/plugins/`: Define `Plugin(ABC)` base class with hooks: `before_scrape(url: str)`, `after_scrape(html: str)`, `before_process(html: str)`, `after_process(result: Any)`, `on_error(error: Exception)`. Create `PluginManager` to register and execute plugins. Implement discovery mechanism to load plugins from `plugins/` directory. Add example plugins: `LoggingPlugin` (logs all operations), `MetricsPlugin` (collects timing metrics), `CachePlugin` (caches results). Update `ScrapingService` to integrate plugin hooks at appropriate points. Document plugin development guide.                                                            |           |      |
| TASK-036 | Add progress tracking to `scraping_service.py`: Create `ProgressTracker` class with methods: `start(total_steps: int)`, `update(current_step: int, message: str)`, `complete()`. Support callbacks for progress updates. Add progress tracking to scrape_and_process: Track steps (browser init, navigation, content extraction, screenshot, LLM processing). Emit progress events at each step. Support optional progress_callback parameter in `scrape_and_process()`. Implement progress bar for CLI using `tqdm`. Create progress event types: `ProgressEvent(step: int, total: int, message: str, timestamp: datetime)`. Enable streaming progress updates for long-running operations. |           |      |

### Implementation Phase 7: Production Readiness

- GOAL-007: Prepare application for production deployment with monitoring, metrics, and operational excellence

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Completed | Date |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ---- |
| TASK-037 | Create structured logging configuration in `src/ai_browser_agent/utils/logging_config.py`: Configure `logging` with JSON formatters for production using `python-json-logger`. Add correlation IDs to track requests across components. Configure log rotation using `RotatingFileHandler` with max size 10MB, 5 backup files. Support different outputs: console (development), file (production), structured JSON (production). Add logging context manager to attach metadata. Create logger factory function: `get_logger(name: str) -> logging.Logger`. Configure log levels per module in settings.                   |           |      |
| TASK-038 | Add metrics collection in `src/ai_browser_agent/utils/metrics.py`: Create `MetricsCollector` class to track: scraping duration, processing duration, token usage, error rates, cache hit rates, browser pool utilization. Use `dataclasses` for metric data structures. Implement methods: `record_scraping_duration(url: str, duration: float)`, `record_processing_duration(model: str, tokens: int, duration: float)`, `record_error(error_type: str, context: Dict)`. Store metrics in-memory with time-series data. Add method to export metrics as JSON or Prometheus format. Implement periodic metrics reporting. |           |      |
| TASK-039 | Create health check endpoint in `src/ai_browser_agent/utils/health.py`: `HealthChecker` class with methods: `check_browser() -> bool` (verify Playwright is installed), `check_openai_api() -> bool` (verify API key and connectivity), `check_dependencies() -> Dict[str, bool]` (check all external dependencies). Implement `get_health_status() -> HealthStatus` that returns: `status: str` (healthy/degraded/unhealthy), `checks: Dict[str, CheckResult]`, `timestamp: datetime`, `version: str`. Add endpoint for monitoring systems to query.                                                                          |           |      |
| TASK-040 | Create Docker support: Add `Dockerfile` with multi-stage build (build stage for dependencies, runtime stage for application). Use Python 3.10 slim base image. Install Playwright browsers in build stage. Copy only necessary files to runtime stage. Set proper user permissions (non-root user). Expose health check port. Add `.dockerignore` excluding `.venv`, `__pycache__`, `.git`, `tests/`, `.env`, etc. Add `docker-compose.yml` for local development with services: app, redis (for caching), prometheus (for metrics). Include environment variable configuration in compose file.                             |           |      |
| TASK-041 | Add caching layer in `src/ai_browser_agent/utils/cache.py`: Create `CacheManager` class supporting multiple backends: `MemoryCache` (in-process LRU cache using `functools.lru_cache`), `RedisCache` (distributed cache using `redis-py`). Implement methods: `async def get(key: str) -> Optional[Any]`, `async def set(key: str, value: Any, ttl: int)`, `async def delete(key: str)`, `async def clear()`. Add cache decorator `@cached` for functions. Configure TTL per cache type: HTML content 1 hour, LLM results 24 hours. Add cache key generation from URL and parameters.                                      |           |      |
| TASK-042 | Create CLI interface in `src/ai_browser_agent/cli.py`: Use `click` library to create command-line interface. Add commands: `scrape` (scrape single URL), `batch` (scrape multiple URLs from file), `config` (show/validate configuration), `health` (run health checks), `version` (show version info). Add options: `--url`, `--output` (JSON/CSV), `--model`, `--provider`, `--headless`, `--verbose`. Implement proper error handling and user-friendly output. Add progress bars for batch operations. Support reading URLs from stdin for piping. Add `--dry-run` flag to validate without executing.                          |           |      |

### Implementation Phase 8: Documentation & Examples

- GOAL-008: Create comprehensive documentation, tutorials, and example use cases for the refactored application

| Task     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Completed | Date |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| TASK-043 | Create comprehensive API documentation in `docs/` directory: `docs/api/web_scraper.md` documenting `WebScraperAgent` class methods, parameters, return types, examples. `docs/api/llm_processor.md` documenting processor classes and factory. `docs/api/scraping_service.md` documenting orchestration service. `docs/api/models.md` documenting Pydantic models. Use Markdown format with code examples. Include complete working examples for each major class. Document all exceptions that may be raised.                                                                           |           |      |
| TASK-044 | Create architecture documentation in `docs/architecture.md`: Describe high-level system architecture with diagrams (use Mermaid format), explain component interactions and data flow, document design decisions and trade-offs, describe extension points (plugins, custom processors), include sequence diagrams for main workflows (scraping, processing), document error handling flow. Add system context diagram showing external dependencies.                                                                                                                                     |           |      |
| TASK-045 | Create usage tutorials in `docs/tutorials/`: `01-getting-started.md` (basic setup and first scrape), `02-custom-models.md` (defining custom Pydantic models), `03-error-handling.md` (handling errors gracefully), `04-configuration.md` (configuring for different environments), `05-plugins.md` (creating custom plugins), `06-batch-processing.md` (scraping multiple URLs efficiently), `07-production-deployment.md` (deploying with Docker, monitoring, scaling). Each tutorial should be self-contained with complete working code examples.                                   |           |      |
| TASK-046 | Create example scripts in `examples/` directory: `examples/basic_scraping.py` (simple single-page scrape), `examples/custom_model.py` (using custom Pydantic models), `examples/batch_scraping.py` (scraping multiple URLs with concurrency), `examples/with_caching.py` (using cache layer), `examples/progress_tracking.py` (tracking progress with callbacks), `examples/custom_plugin.py` (implementing custom plugin), `examples/multi_provider.py` (using different LLM providers). Each example should be fully functional and documented with inline comments.                |           |      |
| TASK-047 | Update main `README.md` with refactored project structure: Update installation instructions for new structure, add badges (build status, coverage, version, license), update API usage examples to use new imports, add links to detailed documentation in `docs/`, add quick start section with minimal example, add features section highlighting new capabilities (multi-provider, plugins, caching, CLI), add troubleshooting section for common issues, update project structure diagram, add section on running tests and contributing.                                           |           |      |
| TASK-048 | Create migration guide update `MIGRATION_GUIDE_V2.md`: Document migration from current structure to refactored structure, provide mapping of old imports to new imports, document breaking changes with before/after examples, provide automated migration script if possible, document new features and how to adopt them, add FAQ section for common migration questions. Include checklist for migration steps. Provide timeline and deprecation notices for old APIs.                                                                                                                 |           |      |

## 3. Alternatives

### Alternative Approaches Considered

- **ALT-001**: Use Django/Flask for web service instead of CLI - Rejected because the core use case is programmatic usage and CLI, not web service. Can be added later as an extension.

- **ALT-002**: Use langchain or llamaindex instead of custom LLM processing - Rejected because current implementation is simpler and more focused. These frameworks add complexity and dependencies that aren't needed for structured extraction.

- **ALT-003**: Use Scrapy instead of Playwright - Rejected because Playwright provides better JavaScript rendering and browser automation capabilities needed for modern web applications.

- **ALT-004**: Store configuration in database instead of files - Rejected for initial refactoring. File-based configuration is simpler for most use cases. Database config can be added as a plugin later.

- **ALT-005**: Use Poetry instead of pip for dependency management - Considered but rejected to maintain compatibility with existing workflows. Poetry can be adopted in future if pip becomes limiting.

- **ALT-006**: Implement GraphQL API instead of REST - Not applicable for current scope which focuses on Python library and CLI, not web service.

## 4. Dependencies

### New Dependencies to Add

- **DEP-001**: `pytest-asyncio>=0.21.0` - Async test support
- **DEP-002**: `pytest-cov>=4.1.0` - Code coverage reporting
- **DEP-003**: `pytest-mock>=3.11.0` - Mocking utilities for tests
- **DEP-004**: `pytest-xdist>=3.3.0` - Parallel test execution
- **DEP-005**: `black>=23.0.0` - Code formatting
- **DEP-006**: `isort>=5.12.0` - Import sorting
- **DEP-007**: `flake8>=6.0.0` - Linting
- **DEP-008**: `mypy>=1.4.0` - Static type checking
- **DEP-009**: `pydantic-settings>=2.0.0` - Settings management with Pydantic
- **DEP-010**: `python-json-logger>=2.0.0` - JSON logging for production
- **DEP-011**: `click>=8.1.0` - CLI framework
- **DEP-012**: `redis>=4.5.0` - Optional caching backend
- **DEP-013**: `instructor>=0.4.0` - Structured outputs from LLMs
- **DEP-014**: `anthropic>=0.18.0` - Anthropic API client (optional)
- **DEP-015**: `tqdm>=4.65.0` - Progress bars for CLI

### Dependency Version Updates

- **DEP-016**: Update `openai` to latest version with structured output support
- **DEP-017**: Update `playwright` to latest stable version
- **DEP-018**: Update `pydantic` to v2.x if not already updated
- **DEP-019**: Update `tiktoken` to latest version for token counting

### External Dependencies

- **DEP-020**: Playwright browsers must be installed via `playwright install`
- **DEP-021**: Redis server (optional, for distributed caching)
- **DEP-022**: Docker and Docker Compose (optional, for containerized deployment)

## 5. Files

### New Files to Create

- **FILE-001**: `pyproject.toml` - Package configuration and tool settings
- **FILE-002**: `setup.py` or use `pyproject.toml` only with PEP 621
- **FILE-003**: `.python-version` - Python version specification
- **FILE-004**: `requirements-dev.txt` - Development dependencies
- **FILE-005**: `requirements-test.txt` - Testing dependencies
- **FILE-006**: `Makefile` or `justfile` - Development task automation
- **FILE-007**: `.env.example` - Example environment variables
- **FILE-008**: `pytest.ini` - Pytest configuration
- **FILE-009**: `.flake8` - Flake8 configuration
- **FILE-010**: `CONTRIBUTING.md` - Contribution guidelines
- **FILE-011**: `Dockerfile` - Container build instructions
- **FILE-012**: `docker-compose.yml` - Local development environment
- **FILE-013**: `.dockerignore` - Docker build exclusions
- **FILE-014**: `src/ai_browser_agent/__init__.py` - Package initialization
- **FILE-015**: `src/ai_browser_agent/exceptions.py` - Custom exceptions
- **FILE-016**: `src/ai_browser_agent/config/settings.py` - Settings management
- **FILE-017**: `src/ai_browser_agent/config/environments.py` - Environment configs
- **FILE-018**: `src/ai_browser_agent/utils/retry.py` - Retry utilities
- **FILE-019**: `src/ai_browser_agent/utils/logging_config.py` - Logging configuration
- **FILE-020**: `src/ai_browser_agent/utils/metrics.py` - Metrics collection
- **FILE-021**: `src/ai_browser_agent/utils/health.py` - Health checks
- **FILE-022**: `src/ai_browser_agent/utils/cache.py` - Caching layer
- **FILE-023**: `src/ai_browser_agent/processors/base.py` - Base processor interface
- **FILE-024**: `src/ai_browser_agent/processors/openai.py` - OpenAI processor
- **FILE-025**: `src/ai_browser_agent/processors/anthropic.py` - Anthropic processor
- **FILE-026**: `src/ai_browser_agent/processors/factory.py` - Processor factory
- **FILE-027**: `src/ai_browser_agent/scrapers/browser_pool.py` - Browser pooling
- **FILE-028**: `src/ai_browser_agent/plugins/__init__.py` - Plugin system
- **FILE-029**: `src/ai_browser_agent/cli.py` - Command-line interface
- **FILE-030**: `tests/conftest.py` - Pytest fixtures
- **FILE-031**: `tests/unit/test_web_scraper.py` - Web scraper tests
- **FILE-032**: `tests/unit/test_llm_processor.py` - LLM processor tests
- **FILE-033**: `tests/unit/test_scraping_service.py` - Service tests
- **FILE-034**: `tests/integration/test_end_to_end.py` - Integration tests
- **FILE-035**: `docs/architecture.md` - Architecture documentation
- **FILE-036**: `docs/api/web_scraper.md` - API documentation
- **FILE-037**: `docs/api/llm_processor.md` - API documentation
- **FILE-038**: `docs/api/scraping_service.md` - API documentation
- **FILE-039**: `docs/api/models.md` - Models documentation
- **FILE-040**: `docs/tutorials/01-getting-started.md` - Tutorial
- **FILE-041**: `examples/basic_scraping.py` - Example script
- **FILE-042**: `examples/custom_model.py` - Example script
- **FILE-043**: `examples/batch_scraping.py` - Example script
- **FILE-044**: `MIGRATION_GUIDE_V2.md` - Migration documentation

### Files to Modify

- **FILE-045**: `src/config.py` → Move to `src/ai_browser_agent/config/__init__.py`
- **FILE-046**: `src/web_scraper.py` → Move to `src/ai_browser_agent/scrapers/web_scraper.py`
- **FILE-047**: `src/llm_processor.py` → Move to `src/ai_browser_agent/processors/openai.py`
- **FILE-048**: `src/scraping_service.py` → Move to `src/ai_browser_agent/services/scraping_service.py`
- **FILE-049**: `src/models.py` → Move to `src/ai_browser_agent/models/__init__.py`
- **FILE-050**: `src/helpers.py` → Move to `src/ai_browser_agent/utils/helpers.py`
- **FILE-051**: `src/main.py` → Update imports and keep as entry point
- **FILE-052**: `README.md` - Update with new structure and features
- **FILE-053**: `requirements.txt` - Split and reorganize dependencies
- **FILE-054**: `.gitignore` - Add new cache and build directories

## 6. Testing

### Unit Tests Required

- **TEST-001**: Test `Settings` class loads from environment variables correctly
- **TEST-002**: Test `Settings` validation rejects invalid configurations
- **TEST-003**: Test environment-specific configurations override defaults correctly
- **TEST-004**: Test custom exception hierarchy and context preservation
- **TEST-005**: Test retry decorator with exponential backoff and jitter
- **TEST-006**: Test circuit breaker opens/closes based on failure threshold
- **TEST-007**: Test `WebScraperAgent` context manager cleanup
- **TEST-008**: Test browser pooling acquire/release cycle
- **TEST-009**: Test token counting accuracy with tiktoken
- **TEST-010**: Test HTML truncation preserves structure
- **TEST-011**: Test processor factory creates correct processor instances
- **TEST-012**: Test OpenAI processor with mocked API responses
- **TEST-013**: Test Anthropic processor with mocked API responses
- **TEST-014**: Test plugin system registers and executes hooks correctly
- **TEST-015**: Test progress tracker emits events at correct intervals
- **TEST-016**: Test metrics collector records and aggregates data
- **TEST-017**: Test health checker verifies all dependencies
- **TEST-018**: Test cache manager with both memory and Redis backends
- **TEST-019**: Test CLI commands with various options
- **TEST-020**: Test error propagation through the stack

### Integration Tests Required

- **TEST-021**: Test complete scraping flow with real browser and mocked LLM
- **TEST-022**: Test batch scraping with multiple URLs
- **TEST-023**: Test concurrent scraping operations with browser pool
- **TEST-024**: Test plugin hooks are called in correct order
- **TEST-025**: Test configuration changes affect runtime behavior
- **TEST-026**: Test graceful degradation when optional dependencies unavailable
- **TEST-027**: Test cache invalidation and TTL expiration
- **TEST-028**: Test health check endpoint returns correct status
- **TEST-029**: Test metrics export in Prometheus format
- **TEST-030**: Test CLI batch command with progress tracking

### Performance Tests

- **TEST-031**: Benchmark HTML truncation performance with large documents
- **TEST-032**: Measure browser pool overhead vs single browser
- **TEST-033**: Test memory usage under sustained load
- **TEST-034**: Benchmark token counting performance
- **TEST-035**: Measure LLM API call latency and retry overhead

### Test Coverage Goals

- **TEST-036**: Achieve minimum 80% overall test coverage
- **TEST-037**: Achieve 90%+ coverage for core modules (scrapers, processors, services)
- **TEST-038**: Achieve 100% coverage for critical paths (error handling, retry logic)

## 7. Risks & Assumptions

### Technical Risks

- **RISK-001**: Breaking changes in refactoring may affect existing users - Mitigation: Maintain backward compatibility layer, provide migration guide and automated migration tools
- **RISK-002**: New dependencies may introduce security vulnerabilities - Mitigation: Use `safety` or `pip-audit` to scan for vulnerabilities, pin dependencies with hash verification
- **RISK-003**: Browser pooling may introduce resource leaks - Mitigation: Implement comprehensive resource cleanup, add leak detection in tests, include monitoring metrics
- **RISK-004**: Token counting may not be accurate for all models - Mitigation: Implement fallback estimation, allow custom token counters, add buffer margin to limits
- **RISK-005**: Plugin system may be exploited for malicious code execution - Mitigation: Implement plugin sandboxing, require explicit plugin registration, document security best practices
- **RISK-006**: Retry logic may cause cascading failures under high load - Mitigation: Implement exponential backoff with jitter, circuit breakers, rate limiting
- **RISK-007**: Caching may return stale data - Mitigation: Implement cache invalidation strategies, configurable TTL, cache versioning

### Operational Risks

- **RISK-008**: Docker images may be large due to Playwright browsers - Mitigation: Use multi-stage builds, consider using pre-built browser images, optimize layer caching
- **RISK-009**: Migration may be time-consuming for large codebases - Mitigation: Provide automated migration script, support both old and new APIs during transition period
- **RISK-010**: Documentation may become outdated quickly - Mitigation: Include documentation updates in PR requirements, generate API docs from code, regular documentation reviews

### Assumptions

- **ASSUMPTION-001**: Users are running Python 3.8 or higher - Validation: Test on multiple Python versions in CI
- **ASSUMPTION-002**: Users have sufficient resources to run Playwright browsers - Validation: Document minimum system requirements
- **ASSUMPTION-003**: OpenAI API remains stable and backward compatible - Validation: Pin API version, monitor API changes, implement adapter pattern for API changes
- **ASSUMPTION-004**: Users primarily scrape HTML content, not complex SPAs requiring extensive JavaScript execution - Validation: Add configurable wait strategies for different page types
- **ASSUMPTION-005**: Redis is available for distributed caching (optional) - Validation: Make Redis optional, fallback to memory cache
- **ASSUMPTION-006**: Users can tolerate eventual consistency in cached results - Validation: Document caching behavior, provide cache invalidation methods
- **ASSUMPTION-007**: Browser automation requirements won't change drastically - Validation: Abstract browser interface to allow switching implementations

## 8. Related Specifications / Further Reading

### Internal Documentation

- [Current Project README](../README.md) - Current project structure and usage
- [Migration Guide](../MIGRATION_GUIDE.md) - Previous migration documentation
- [Copilot Instructions](../.github/copilot-instructions.md) - Development guidelines and patterns

### External References

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Configuration management
- [Playwright Python Documentation](https://playwright.dev/python/) - Browser automation
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) - Structured data extraction
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api) - Alternative LLM provider
- [Python Packaging User Guide](https://packaging.python.org/) - Package distribution best practices
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [Black Code Style](https://black.readthedocs.io/) - Code formatting
- [mypy Documentation](https://mypy.readthedocs.io/) - Static type checking
- [The Twelve-Factor App](https://12factor.net/) - Production application principles
- [Python Design Patterns](https://refactoring.guru/design-patterns/python) - Design patterns reference
