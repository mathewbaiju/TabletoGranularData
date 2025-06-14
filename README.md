# Table to Granular Data Analyzer

## Overview
This tool helps Program Managers analyze and visualize ownership distribution across teams. It's particularly useful for understanding resource allocation, workload distribution, and identifying potential bottlenecks in team assignments.

## Key Features

### 📊 Ownership Analysis
- Processes CSV files containing ownership data
- Handles complex data formats including hyperlinked names
- Supports UTF-16 encoding and tab-separated files
- Automatically cleans and standardizes data

### 📈 Distribution Insights
- Calculates total items per owner
- Provides detailed distribution statistics
- Shows workload patterns across teams
- Identifies concentration of responsibilities

### 🔍 Key Metrics
- Total items and unique owners
- Items per owner (min/max/average)
- Detailed breakdown by ownership level
- Complete distribution analysis

### 💬 Slack Integration
- Generates Slack-friendly formatted reports
- Supports @mentions for easy team communication
- Creates well-organized, hierarchical summaries
- Enables easy sharing of analysis results

## Sample Output
The tool provides insights such as:
- Total number of items and unique owners
- Distribution of items (e.g., "14 items: 1 person", "8 items: 1 person", etc.)
- Average items per owner
- Complete list of owners grouped by workload
- Summary statistics and distribution patterns

## Use Cases

### 1. Resource Planning
- Understand current workload distribution
- Identify heavily loaded team members
- Plan resource reallocation
- Track ownership patterns

### 2. Team Analysis
- Review team capacity
- Identify potential bottlenecks
- Support workload balancing decisions
- Monitor distribution changes over time

### 3. Project Management
- Track item ownership
- Generate stakeholder reports
- Facilitate team discussions
- Support data-driven decisions

## Getting Started

1. Place your CSV file in the project directory
2. Run the analysis script:
   ```bash
   python3 extract_owners.py
   ```
3. Find the formatted results in:
   - Terminal output for detailed analysis
   - `slack_message.txt` for Slack-ready format

## Data Requirements
The CSV file should include:
- Owner/Contact Person column
- One row per item
- UTF-16 encoding (preferred)
- Tab-separated values

## Output Options
1. **Detailed Analysis**: Complete statistical breakdown
2. **Slack Format**: Ready-to-share team updates
3. **Distribution Summary**: Quick overview of allocation
4. **Owner Lists**: Grouped by number of items

## Benefits
- 📊 Data-driven decision making
- 🎯 Clear ownership visibility
- 📈 Easy progress tracking
- 🤝 Better team communication
- ⚖️ Workload balancing support

## Technical Notes
- Supports various CSV formats
- Handles special characters
- Processes hyperlinked content
- Maintains data integrity 