# Source Roadmap for Foundry Stack

This file tracks where to find authoritative answers for each glossary topic. The goal is to make every `.md` entry traceable to source types before writing the final definitions.

## Source Tiers

- **Tier 1 primary**: company annual reports/20-F/10-K, investor presentations, earnings transcripts, official government reports, standards bodies, vendor documentation.
- **Tier 2 institutional**: CSET, OECD, SIA, SEMI, IEEE/IRDS, imec, academic papers, reputable university reports.
- **Tier 3 secondary**: SemiAnalysis, industry press, analyst reports, vendor blogs, textbooks/primers.

## Core Sources Already Found by Sherlock

Transcript: `.pi-sherlock/sherlock-20260505-145141.md`

1. U.S. DOE, **Semiconductor Supply Chain Deep Dive Assessment**  
   Local copy: `sources/Semiconductor%20Supply%20Chain%20Report%20-%20Final[1].pdf`  
   URL: https://www.energy.gov/sites/default/files/2024-12/Semiconductor%2520Supply%2520Chain%2520Report%2520-%2520Final%5B1%5D.pdf  
   **Scope note:** this is not a general foundry primer. It is an energy-sector semiconductor supply-chain report with a strong focus on conventional semiconductors plus wide bandgap (WBG) power electronics, especially SiC and GaN for EVs, charging, renewables, grid/HVDC, industrial power, and power modules.
2. CSET Georgetown, **AI Chips: What They Are and Why They Matter**  
   https://cset.georgetown.edu/wp-content/uploads/AI-Chips%E2%80%94What-They-Are-and-Why-They-Matter-1.pdf
3. OSTI-hosted semiconductor supply-chain / AI hardware source  
   https://www.osti.gov/pages/servlets/purl/1847077

Sherlock also identified unfetched leads:

- CSET, **The Semiconductor Supply Chain Issue Brief**  
  https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief.pdf
- White House, **100-Day Supply Chain Review Report**  
  https://www.whitehouse.gov/wp-content/uploads/2021/06/100-day-supply-chain-review-report.pdf
- Princeton supply-chain paper  
  https://parallel.princeton.edu/papers/supply_chain.pdf

## High-Value Primary Sources to Add

### Foundry company disclosures

Use for market structure, operating model, metrics, utilization, capacity, node mix, revenue by application/region.

- TSMC annual reports / Form 20-F: https://investor.tsmc.com/english/annual-reports
- TSMC quarterly results and earnings transcripts: https://investor.tsmc.com/english/quarterly-results
- UMC annual reports: https://www.umc.com/en/IR_FinancialReports/annual_reports
- GlobalFoundries SEC filings: https://www.sec.gov/edgar/browse/?CIK=1709048
- SMIC annual/interim reports: https://www.smics.com/en/site/company_financialSummary
- Samsung Electronics annual reports: https://www.samsung.com/global/ir/reports-disclosures/annual-reports/
- Intel annual reports / foundry disclosures: https://www.intc.com/filings-reports/annual-reports-proxies

### Equipment vendor disclosures and technical pages

Use for fab system, bottleneck tools, EUV/DUV, etch, deposition, CMP, metrology.

- ASML annual reports and technology pages: https://www.asml.com/en/investors/annual-report
- ASML EUV lithography: https://www.asml.com/en/technology/lithography-principles/euv-lithography
- Applied Materials annual reports: https://ir.appliedmaterials.com/financial-information/annual-reports
- Lam Research annual reports: https://investor.lamresearch.com/financial-information/annual-reports
- KLA annual reports: https://ir.kla.com/financials/annual-reports
- Tokyo Electron annual reports: https://www.tel.com/ir/library/ar/
- SCREEN annual reports: https://www.screen.co.jp/en/ir/library/annual

### Industry organizations / standards / roadmaps

Use for process nodes, roadmaps, capacity definitions, WSPM, supply-chain structure.

- SIA reports: https://www.semiconductors.org/resources/
- SEMI market data and reports: https://www.semi.org/en/market-data
- IEEE IRDS roadmap: https://irds.ieee.org/
- imec technology insights: https://www.imec-int.com/en/articles
- SEMI E84 / AMHS / FOUP standards references via SEMI standards catalog.

## Topic-by-Topic Source Map

### Market Structure

| Topic | Best source types | Specific leads |
|---|---|---|
| Foundry | TSMC/UMC/GF annual reports; SIA/CSET primers | TSMC 20-F business overview; CSET supply-chain issue brief |
| Pure-Play Foundry | TSMC/UMC/GF reports; industry primers | TSMC annual report; GlobalFoundries 10-K |
| IDM | Intel/Samsung annual reports; SIA primers | Intel 10-K; Samsung annual report |
| Fabless Company | SIA/CSET primers; Nvidia/AMD/Qualcomm filings | CSET AI Chips; Nvidia 10-K business model |
| Merchant Capacity | Foundry annual reports; analyst definitions | TSMC/GF filings; SIA industry reports |
| Captive Capacity | IDM filings; Intel/Samsung reports | Intel 10-K manufacturing strategy; Samsung reports |
| Customer Concentration | Company annual reports; 20-F risk factors | TSMC customer concentration; GF 10-K customer concentration |
| End Market | Foundry revenue segmentation | TSMC platform revenue; GF end-market disclosures |
| Application Mix | Foundry quarterly decks | TSMC HPC/smartphone/auto/IoT/DCE split |
| Regional Mix | Annual reports; revenue by geography | TSMC/GF/UMC geographic revenue tables |

### Fab System

| Topic | Best source types | Specific leads |
|---|---|---|
| Fab | Company annual reports; DOE/SIA primers | TSMC annual report; DOE supply-chain report |
| Cleanroom | SEMI/technical primers; fab construction sources | SEMI; ASML/Applied Materials education pages |
| Wafer | SEMI/SIA primers; company reports | SEMI silicon wafer data; SUMCO/Shin-Etsu reports |
| Tool | Equipment vendor filings | ASML, AMAT, Lam, KLA annual reports |
| Toolset | Equipment vendor filings; process-flow primers | AMAT/Lam/KLA reports; imec articles |
| EUV Scanner | ASML primary sources | ASML annual report; ASML EUV technology page |
| DUV Scanner | ASML/Nikon/Canon sources | ASML DUV page; ASML annual report |
| Etch Tool | Lam/AMAT/TEL sources | Lam annual report; Applied Materials reports |
| Deposition Tool | AMAT/Lam/TEL sources | Applied Materials annual report; Lam deposition pages |
| CMP Tool | Applied Materials/Ebara sources | AMAT filings; Ebara reports |
| Metrology Tool | KLA/ASML/Hitachi sources | KLA annual report; ASML metrology pages |
| FOUP | SEMI standards; AMHS vendor pages | SEMI standards; Brooks/Daifuku/Muratec pages |
| AMHS | SEMI standards; AMHS vendor disclosures | Daifuku annual report; SEMI E84 references |
| Installed Capacity | Foundry filings; SEMI capacity reports | TSMC/UMC reports; SEMI fab data |
| Effective Capacity | Company commentary; utilization/cycle-time models | TSMC calls; SEMI reports; modeling assumptions |

### Process Stack

| Topic | Best source types | Specific leads |
|---|---|---|
| Process Node | IRDS; foundry technology pages | TSMC technology pages; IRDS roadmap |
| Mature Node | Foundry disclosures; SIA/SEMI reports | UMC/SMIC reports; TSMC specialty tech |
| Leading-Edge Node | TSMC/Samsung/Intel disclosures | TSMC N3/N2 pages; Intel process roadmap |
| Node Mix | Foundry revenue by technology | TSMC revenue by technology tables |
| FinFET | Foundry tech pages; textbooks; IEEE | TSMC FinFET pages; IRDS |
| GAAFET | Samsung/TSMC/Intel tech pages; imec | Samsung GAA pages; TSMC N2 nanosheet comments; imec |
| Backside Power Delivery | Intel/imec/TSMC technical disclosures | Intel PowerVia; imec backside power articles |
| EUV Layer | ASML/foundry technical disclosures | ASML EUV pages; TSMC/Samsung node disclosures |
| Mask Set | Lithography/process primers; mask vendor reports | Photronics/Toppan/Hoya reports; ASML lithography primers |
| Yield | Foundry filings; process-control textbooks | TSMC annual report risk factors; KLA process control material |
| Yield Ramp | Foundry earnings calls; annual reports | TSMC quarterly calls; Intel/Samsung ramp commentary |
| Process Roadmap | IRDS; foundry roadmaps | IRDS; TSMC tech symposium; Intel roadmaps |

### Operating Model

| Topic | Best source types | Specific leads |
|---|---|---|
| Wafer Start | SEMI; foundry disclosures | SEMI fab data; TSMC capacity commentary |
| WSPM | SEMI/foundry reports | SEMI capacity definitions; foundry annual reports |
| Wafer Shipment | Foundry reports; silicon wafer suppliers | UMC/GF/SMIC shipments; SEMI silicon shipment data |
| Utilization | Earnings calls; annual reports | TSMC/UMC/GF quarterly commentary |
| Cycle Time | Fab operations textbooks; academic papers | Factory Physics; semiconductor manufacturing operations literature |
| Ramp | Earnings calls; annual reports | TSMC new node ramp commentary |
| Capacity Expansion | Capex plans; fab announcements | TSMC Arizona/Japan/Germany; Intel fabs; Samsung fabs |
| Tool-Limited Capacity | Equipment lead-time commentary | ASML backlog; Lam/AMAT/KLA lead times; foundry calls |
| Bottleneck Tool | Equipment intensity and backlog | ASML EUV backlog; KLA inspection constraints |
| Inventory | Company balance sheets and footnotes | Annual reports: inventory accounting and DOI inputs |
| DOI | Financial statements; model definition | Inventory / COGS * days; company 20-F/10-K |

### Metrics

| Topic | Best source types | Specific leads |
|---|---|---|
| Foundry Revenue | Income statements; segment reporting | TSMC/UMC/GF/SMIC reports |
| Wafer Revenue | Foundry revenue tables and model assumptions | Revenue minus non-wafer revenue where disclosed |
| Non-Wafer Revenue | Annual report segment notes | TSMC other revenue; mask/service revenue notes |
| Wafer ASP | Revenue and wafer shipment disclosures | UMC/GF reports; model-derived TSMC ASP |
| Capex | Cash-flow statements; capex guidance | TSMC quarterly deck; annual reports |
| R&D | Income statement notes | TSMC/GF/UMC R&D expense |
| COGS | Income statement | Annual reports |
| COGS per Wafer | COGS plus shipment/capacity data | Derived metric; needs methodology note |
| Depreciation | Cash-flow statements; PPE notes | Annual report depreciation/amortization |
| Gross Margin | Income statement | Company reports and quarterly decks |
| Operating Margin | Income statement | Company reports and quarterly decks |
| Revenue by Application | Foundry quarterly decks | TSMC platform revenue |
| Revenue by Region | Annual reports | Geographic revenue tables |
| Historical Data | Company filings; downloaded time series | Annual reports, quarterly decks, model database |
| Forecast Horizon | Model convention; analyst reports | Internal methodology; consensus reports as secondary |

### Models

| Topic | Best source types | Specific leads |
|---|---|---|
| Foundry Metrics Model | Company financials; methodology note | TSMC/UMC/GF/SMIC filings; internal model docs |
| Capacity-Demand Model | SEMI capacity; end-market demand; foundry shipments | SEMI, WSTS, company reports |
| Customer Allocation Model | Customer concentration; end-market shipment estimates | Foundry customer disclosures; fabless company COGS/inventory |
| Wafer Starts by Customer | Foundry customer concentration; fabless wafer demand estimates | TSMC customer notes; Nvidia/Apple/AMD/Qualcomm filings |
| Wafer Starts by End Market | Application mix; die size/wafer assumptions | TSMC application mix; model methodology |
| Demand Forecast | WSTS, Gartner/IDC/Omdia, company guidance | WSTS public releases; company guidance |
| Capacity Forecast | Capex/fab buildouts/equipment deliveries | SEMI fab forecast; ASML shipments; foundry capex |
| Utilization Curve | Historical utilization vs revenue/capacity | Company calls; internal fitted curve |
| Node Cost Model | Process cost papers; industry reports | IRDS, imec, IBS/VLSI secondary if available |
| Fab P&L Model | Company financial statements; cost accounting | Income statement, capex, depreciation, utilization assumptions |
| Methodology and Definitions | All above; glossary source notes | This roadmap plus explicit formulas |

## Recommended Workflow for Each `.md`

1. Add a `## Definition` section.
2. Add a `## Why it matters` section for foundry analysis.
3. Add a `## Where to find it` section listing exact source types and URLs.
4. Add a `## Related terms` section using internal links.
5. Add footnotes or source links inline.

Example:

```md
## Where to find it

- TSMC annual reports: source for foundry revenue, node mix, capex, and utilization commentary.
- ASML annual reports: source for EUV scanner shipments, backlog, and lithography bottlenecks.
- SEMI fab data: source for WSPM and installed capacity definitions.
```
