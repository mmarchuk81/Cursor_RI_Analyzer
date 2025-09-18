"""
# Cursor_RI_Analyzer — US Rental Real Estate Risk Analyzer
This app is designed for an investor in the US real estate rental market.

## Objective
Decrease risks by 10–15% by obtaining full analytical and regulatory data on the market.

## Investor Strategy A
- Combination of appreciation and cash flow with priority toward cash flow
- Good schools to attract families with kids for long-term rent (ideally 5+ years)
- Regulatory focus
- Price 250–300K USD
- Diversified employer base by top employers
- Best scoring based on analytics on market fundamentals, housing market conditions, crime rate and any XFactors

## Input
- City, State (for example: Lockhart, TX)

## Output
- Full range of market fundamentals, housing market conditions, top employers, public schools, regulatory environment, crime rate, and X-factors

## Current module level
- data/ — placeholder for datasets, cached API responses, or exports (CSV/JSON). Keep large files out of git with .gitignore.
- src/ — application source code (clients, metrics, CLI entry, helpers).
- tests/unit — unit tests and smoke checks.
- requirements.txt — Python dependencies for local dev and CI.
- check_import.py — quick utility script to verify imports resolve in the current environment (used during early setup).

Inside src/ (by responsibility)
- app.py — CLI entry point that orchestrates the run:
  - gets user input (city, state)
  - initializes API clients and helpers (FREDClient, ClaudeClient, RealEstateMetrics, InvestmentScore)
  - Phase 1: market fundamentals (FRED)
  - Phase 2: employers, schools, regulatory, x-factors (Claude summaries)
  - Phase 3: real-estate metrics (sales, rent, ratios)
  - prints a combined summary and recommendation score

- fred_client.py — typed FRED API client wrapping series retrieval and basic MSA mapping:
  - class FREDClient
    - __init__(api_key) — stores key, initializes fredapi.Fred, sets up logging and an MSA mapping
    - _load_msa_mapping() — returns a small city→MSA code dict used by this prototype
    - _get_msa_code(city, state) — normalizes and looks up an MSA code
    - get_series_data(series_id, start_date=None, end_date=None) — calls FRED series/observations with pagination trimmed to recent points
    - get_city_data(city, state) — example of deriving a series_id from a city’s MSA code and returning recent observations

- FRED_utils.py — lightweight helper wrapper around the FRED series/observations REST endpoint:
  - class FREDClient (utility flavor used for direct HTTP requests)
    - __init__(api_key) — validates presence of key and sets up logging
    - get_series_data(series_id, start_date=None, end_date=None) — simple GET with JSON parsing and recent-first sort
    - get_city_data(city, state) — placeholder for mapping city/state to MSA and composing responses

- metrics.py — derived, investor-oriented metrics computed from basic inputs:
  - class RealEstateMetrics
    - __init__(api_keys=None) — stores optional API keys and initializes a simple in-memory cache
    - get_sales_metrics(city, state) — returns median and average sale price, inventory, y/y and 5-year price growth (currently mocked with state baselines and random ranges)
    - get_rental_metrics(city, state) — returns monthly rent, rent-to-price ratio, y/y and 5-year rent growth (derived and mocked)
    - calculate_rent_to_price_ratio(monthly_rent, price) — annualized rent divided by price, as a percentage
    - calculate_rent_to_income_ratio(monthly_rent, monthly_income) — renter cost burden as a percentage

- claude_client.py — LLM summaries to transform raw signals into readable insights:
  - class ClaudeClient
    - __init__(api_key) — sets model and client
    - query_claude(prompt) — single-shot text completion helper
    - get_major_employers(city_state) — returns list of large local employers with headcounts and sectors
    - get_crime_data(city_state) — returns narrative plus a coarse safety rating extracted from the text
    - get_school_ranking(city, state) — returns summary plus an education rating and top public schools
    - get_regulatory_environment(city, state) — returns summary, full notes, and a landlord-friendliness rating
    - market_factors(city, state) — returns risks, benefits, and x-factors
    - get_all_quantitative_insights(...) — helper to collate multiple numeric outputs

- scoring.py — investment scoring and recommendation (referenced from app.py):
  - class InvestmentScore
    - calculate_score(market_data, ri_data) — composes a weighted score from fundamentals, housing metrics, and risk flags
    - get_recommendation(overall_score) — maps score to human-readable buy/hold/watch guidance

Tests
- tests/unit/Test_claude.py — unit tests for ClaudeClient behavior with mocks and fixtures (currently includes a few typos to fix as we stabilize)
- tests/test_docs.py — README smoke test that asserts key sections exist 
- tests/test_imports.py — import smoke test to ensure main modules can be imported in CI 


## Planned modules
- openai_utils.py — optional OpenAI helpers for text summaries, embeddings, and classification
- scoring.py — InvestmentScore implementation if not already present; maps metrics to a single recommendation score
- ri_metrics.py — rename or alias to metrics.py so imports are consistent across the app
- data_clients/
  - zillow_client.py — listing and pricing signals (if API/terms allow)
  - redfin_client.py — market activity and inventory
  - realtor_client.py — rent and days-on-market signals
  - schools_client.py — public school ratings and catchments
  - crime_client.py — crime indices aggregation
  - regulators_client.py — landlord rules, eviction timelines, rent control, property taxes
- caching.py — simple TTL cache or disk-backed cache for API responses
- exporters.py — JSON/CSV export of analysis results
- cli.py — argument-parsed CLI wrapper around app.py for non-interactive runs
- config.py — centralized config and environment variable loading (FRED/LLM keys, feature flags)

"""