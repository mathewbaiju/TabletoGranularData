import pandas as pd
import sys
import os
from pathlib import Path
import re
from collections import Counter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def post_to_slack(message, channel, token):
    """
    Post a message to Slack
    Args:
        message: The message to post
        channel: The channel to post to (e.g., '#your-channel')
        token: Slack Bot User OAuth Token
    """
    try:
        client = WebClient(token=token)
        response = client.chat_postMessage(
            channel=channel,
            text=message,
            parse='full'  # This ensures @ mentions are parsed
        )
        print(f"\nMessage posted successfully to {channel}")
        return response
    except SlackApiError as e:
        print(f"\nError posting to Slack: {e.response['error']}")
        return None

def clean_column_name(col):
    # Remove special characters and clean up the column name
    return col.encode('ascii', 'ignore').decode('ascii').strip('"\t ')

def extract_name_from_hyperlink(hyperlink):
    # Extract name from hyperlink format: =HYPERLINK("url";"Name")
    match = re.search(r'=HYPERLINK\("[^"]+";"([^"]+)"\)', hyperlink)
    if match:
        return match.group(1).strip()
    return hyperlink.strip() if isinstance(hyperlink, str) else ''

def format_for_slack(owner_counts, total_items):
    # Create a nicely formatted Slack message
    slack_msg = []
    
    # Header with code block formatting
    slack_msg.append("*API Proxy Ownership Distribution*")
    slack_msg.append(f"Total Items: *{total_items}*\n")
    
    # Sort owners by number of items (descending)
    sorted_owners = sorted(owner_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Group owners by number of items
    items_to_owners = {}
    for owner, count in sorted_owners:
        items_to_owners.setdefault(count, []).append(owner)
    
    # Format the groups
    for item_count in sorted(items_to_owners.keys(), reverse=True):
        owners = items_to_owners[item_count]
        if len(owners) == 1:
            slack_msg.append(f"*{item_count} items:*")
            slack_msg.append(f"• @{owners[0]}")
        else:
            slack_msg.append(f"*{item_count} items: {len(owners)} people*")
            for owner in sorted(owners):
                slack_msg.append(f"• @{owner}")
        slack_msg.append("")  # Add blank line between sections
    
    # Add summary statistics
    unique_owners = len(owner_counts)
    avg_items = total_items / unique_owners
    slack_msg.append("*Summary Statistics:*")
    slack_msg.append(f"• Total unique owners: {unique_owners}")
    slack_msg.append(f"• Average items per owner: {avg_items:.1f}")
    
    # Distribution summary
    distribution = Counter(owner_counts.values())
    slack_msg.append("\n*Distribution:*")
    for item_count in sorted(distribution.keys(), reverse=True):
        owner_count = distribution[item_count]
        slack_msg.append(f"• {item_count} items: {owner_count} {'person' if owner_count == 1 else 'people'}")
    
    # Save as regular message
    with open('slack_message.txt', 'w') as f:
        f.write("\n".join(slack_msg))
    
    # Save as a snippet (with ``` for code block formatting)
    with open('slack_snippet.txt', 'w') as f:
        f.write("```\n")  # Start code block
        f.write("\n".join(slack_msg))
        f.write("\n```")  # End code block
    
    return "\n".join(slack_msg)

def extract_owners(csv_path, owner_column='(D) Contact Person', slack_channel=None, slack_token=None):
    try:
        # Convert to Path object and resolve to absolute path
        csv_path = Path(csv_path).expanduser().resolve()
        print(f"\nTrying to read: {csv_path}")
        
        # Try reading with UTF-16 encoding
        df = pd.read_csv(csv_path, encoding='utf-16', sep='\t')
        
        # Clean up column names
        df.columns = [clean_column_name(col) for col in df.columns]
        
        print("\nAvailable columns in your CSV:")
        print(df.columns.tolist())
        
        # Ask for column name if not found
        if owner_column not in df.columns:
            print(f"\nColumn '{owner_column}' not found in CSV.")
            print("Available columns are:", df.columns.tolist())
            return

        # Show rows with missing owners
        print("\nChecking for rows with missing owners:")
        missing_owners = df[df[owner_column].isna() | (df[owner_column] == '')]
        if not missing_owners.empty:
            print("\nFound rows with missing owners:")
            for idx, row in missing_owners.iterrows():
                print(f"\nRow {idx + 1}:")
                print("Business Service Name:", row['(C) Business Service Name'] if '(C) Business Service Name' in row else 'N/A')
                print("Contact Person:", row[owner_column] if owner_column in row else 'N/A')
                print("Proxy:", row['(A) Proxies'] if '(A) Proxies' in row else 'N/A')
                print("Proxy Repo:", row['(B) Proxy Repo'] if '(B) Proxy Repo' in row else 'N/A')
        else:
            print("No rows with missing owners found.")
        
        # Extract names from hyperlinks
        all_owners = df[owner_column].dropna().apply(extract_name_from_hyperlink)
        
        # Count occurrences of each owner
        owner_counts = Counter(all_owners)
        
        # Get unique owners
        unique_owners = sorted(owner_counts.keys())
        
        # Create Slack message
        slack_message = format_for_slack(owner_counts, len(all_owners))
        
        # Save Slack message to file
        with open('slack_message.txt', 'w') as f:
            f.write(slack_message)
        print("\nSlack message has been saved to 'slack_message.txt'")
        
        # Post to Slack if credentials are provided
        if slack_channel and slack_token:
            post_to_slack(slack_message, slack_channel, slack_token)
        
        # Print original detailed verification
        print("\nDetailed counting verification:")
        print(f"Total rows in CSV: {len(df)}")
        print(f"Rows with non-null owners: {len(df[owner_column].dropna())}")
        
        # Print all rows for verification
        print("\nAll rows with owners (row number: owner):")
        for idx, owner in df[owner_column].dropna().items():
            print(f"Row {idx + 1}: {extract_name_from_hyperlink(owner)}")
        
        print(f"\nFound {len(unique_owners)} unique owners:")
        
        # Print counts and names with verification
        print("\nOwner counts (with verification):")
        running_total = 0
        for owner in unique_owners:
            count = owner_counts[owner]
            running_total += count
            print(f"@{owner}: {count} item{'s' if count > 1 else ''}")
        
        # Print running total
        print(f"\nVerification - Running total of all items: {running_total}")
        
        # Print some statistics
        total_items = sum(owner_counts.values())
        print(f"\nSummary:")
        print(f"Total items (sum of all counts): {total_items}")
        print(f"Total items (running total): {running_total}")
        print(f"Total non-null rows: {len(df[owner_column].dropna())}")
        print(f"Unique owners: {len(unique_owners)}")
        print(f"Average items per owner: {total_items / len(unique_owners):.1f}")
        max_items = max(owner_counts.values())
        owners_with_max = [owner for owner, count in owner_counts.items() if count == max_items]
        print(f"Most items: {max_items} (owned by: {', '.join(f'@{owner}' for owner in owners_with_max)})")
        
        # Print distribution
        print("\nDistribution of items:")
        distribution = Counter(owner_counts.values())
        total_in_distribution = 0
        for item_count in sorted(distribution.keys(), reverse=True):
            owner_count = distribution[item_count]
            total_in_distribution += item_count * owner_count
            print(f"{item_count} items: {owner_count} {'person' if owner_count == 1 else 'people'} (subtotal: {item_count * owner_count})")
        print(f"Distribution total verification: {total_in_distribution}")
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if the file exists:", os.path.exists(csv_path))
        print("2. Check if you have read permissions:", os.access(csv_path, os.R_OK))
        print("3. Try moving the file to a different location")
        sys.exit(1)

if __name__ == "__main__":
    csv_path = "NA items.csv"  # Using relative path in current directory
    
    # Get Slack credentials from environment variables
    slack_channel = os.getenv('SLACK_CHANNEL')
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    
    extract_owners(csv_path, slack_channel=slack_channel, slack_token=slack_token)