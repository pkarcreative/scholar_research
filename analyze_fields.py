import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import seaborn as sns

def load_papers_data(filename):
    """Load papers data from JSON file"""
    papers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    papers.append(json.loads(line))
        print(f"✅ Loaded {len(papers)} papers from {filename}")
        return papers
    except FileNotFoundError:
        print(f"❌ File {filename} not found!")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return []

def analyze_fields_of_study(papers):
    """Analyze the distribution of fields of study"""
    print("\n🔍 Analyzing fields of study...")
    
    # Extract all fields of study
    all_fields = []
    papers_with_fields = 0
    
    for paper in papers:
        if 'fieldsOfStudy' in paper and paper['fieldsOfStudy']:
            fields = paper['fieldsOfStudy']
            if isinstance(fields, list):
                all_fields.extend(fields)
                papers_with_fields += 1
            elif isinstance(fields, str):
                # Handle case where fieldsOfStudy is a string
                all_fields.append(fields)
                papers_with_fields += 1
    
    print(f"📊 Papers with fields of study: {papers_with_fields}/{len(papers)}")
    print(f"🏷️  Total field occurrences: {len(all_fields)}")
    
    if not all_fields:
        print("❌ No fields of study found in the data!")
        return None, None
    
    # Count field occurrences
    field_counts = Counter(all_fields)
    
    # Get top fields
    top_fields = field_counts.most_common(20)
    
    print(f"\n📈 Top 20 fields of study:")
    for i, (field, count) in enumerate(top_fields, 1):
        percentage = (count / len(all_fields)) * 100
        print(f"  {i:2d}. {field:<30} {count:4d} ({percentage:5.1f}%)")
    
    return field_counts, top_fields

def create_visualizations(field_counts, top_fields):
    """Create various visualizations of the field distribution"""
    if not field_counts:
        return
    
    print("\n🎨 Creating visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distribution of Fields of Study in Academic Papers', fontsize=16, fontweight='bold')
    
    # 1. Bar chart of top 15 fields
    top_15 = top_fields[:15]
    fields, counts = zip(*top_15)
    
    bars = ax1.barh(range(len(fields)), counts, color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_yticks(range(len(fields)))
    ax1.set_yticklabels(fields, fontsize=10)
    ax1.set_xlabel('Number of Papers', fontweight='bold')
    ax1.set_title('Top 15 Fields of Study', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax1.text(bar.get_width() + max(counts)*0.01, bar.get_y() + bar.get_height()/2, 
                str(count), ha='left', va='center', fontweight='bold')
    
    # 2. Pie chart of top 10 fields
    top_10 = top_fields[:10]
    pie_fields, pie_counts = zip(*top_10)
    
    # Calculate percentages
    total = sum(pie_counts)
    percentages = [f"{(count/total)*100:.1f}%" for count in pie_counts]
    
    wedges, texts, autotexts = ax2.pie(pie_counts, labels=pie_fields, autopct='%1.1f%%', 
                                       startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Top 10 Fields Distribution', fontweight='bold')
    
    # 3. Horizontal bar chart with percentages
    top_12 = top_fields[:12]
    fields_percent, counts_percent = zip(*top_12)
    percentages_list = [(count/sum(counts_percent))*100 for count in counts_percent]
    
    bars_percent = ax3.barh(range(len(fields_percent)), percentages_list, 
                           color='lightcoral', edgecolor='darkred', alpha=0.7)
    ax3.set_yticks(range(len(fields_percent)))
    ax3.set_yticklabels(fields_percent, fontsize=10)
    ax3.set_xlabel('Percentage of Total Papers (%)', fontweight='bold')
    ax3.set_title('Field Distribution by Percentage', fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    
    # Add percentage labels
    for i, (bar, pct) in enumerate(zip(bars_percent, percentages_list)):
        ax3.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f"{pct:.1f}%", ha='left', va='center', fontweight='bold')
    
    # 4. Cumulative distribution
    sorted_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
    cumulative_counts = []
    field_names = []
    running_total = 0
    
    for field, count in sorted_fields:
        running_total += count
        cumulative_counts.append(running_total)
        field_names.append(field)
    
    # Calculate cumulative percentage
    total_papers = sum(field_counts.values())
    cumulative_percentages = [(count/total_papers)*100 for count in cumulative_counts]
    
    ax4.plot(range(len(cumulative_percentages)), cumulative_percentages, 
             marker='o', linewidth=2, markersize=4, color='green')
    ax4.set_xlabel('Number of Fields', fontweight='bold')
    ax4.set_ylabel('Cumulative Percentage (%)', fontweight='bold')
    ax4.set_title('Cumulative Distribution of Fields', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Add annotations for key points
    for i in [0, len(cumulative_percentages)//4, len(cumulative_percentages)//2, -1]:
        if i < len(cumulative_percentages):
            ax4.annotate(f'{cumulative_percentages[i]:.1f}%', 
                        xy=(i, cumulative_percentages[i]), 
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.show()
    
    # Save the plot
    plt.savefig('fields_of_study_distribution.png', dpi=300, bbox_inches='tight')
    print("💾 Plot saved as 'fields_of_study_distribution.png'")

def filter_by_field(papers, target_field):
    """Filter papers by a specific field of study"""
    filtered_papers = []
    
    for paper in papers:
        if 'fieldsOfStudy' in paper and paper['fieldsOfStudy']:
            fields = paper['fieldsOfStudy']
            if isinstance(fields, list) and target_field in fields:
                filtered_papers.append(paper)
            elif isinstance(fields, str) and target_field in fields:
                filtered_papers.append(paper)
    
    return filtered_papers

def main():
    """Main function to run the analysis"""
    print("🚀 Fields of Study Analysis Tool")
    print("=" * 50)
    
    # Try to load data from different possible files
    possible_files = ['papers.json', 'extended_papers.json']
    papers = []
    
    for filename in possible_files:
        papers = load_papers_data(filename)
        if papers:
            break
    
    if not papers:
        print("❌ No data files found. Please run data_access.py or multi_query_search.py first.")
        return
    
    # Analyze fields of study
    field_counts, top_fields = analyze_fields_of_study(papers)
    
    if not field_counts:
        return
    
    # Create visualizations
    create_visualizations(field_counts, top_fields)
    
    # Interactive field filtering
    print(f"\n🔍 Interactive Field Filtering")
    print("=" * 50)
    
    while True:
        print(f"\nAvailable fields (top 10):")
        for i, (field, count) in enumerate(top_fields[:10], 1):
            print(f"  {i}. {field}")
        
        print(f"  0. Exit")
        
        try:
            choice = input(f"\nSelect a field number to filter papers (0-10): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= 10:
                selected_field = top_fields[choice_num - 1][0]
                filtered_papers = filter_by_field(papers, selected_field)
                
                print(f"\n📊 Papers in '{selected_field}': {len(filtered_papers)}")
                
                if filtered_papers:
                    print(f"\nSample papers:")
                    for i, paper in enumerate(filtered_papers[:5], 1):
                        title = paper.get('title', 'No title')
                        year = paper.get('year', 'No year')
                        print(f"  {i}. {title[:80]}... ({year})")
                    
                    if len(filtered_papers) > 5:
                        print(f"  ... and {len(filtered_papers) - 5} more papers")
                    
                    # Save filtered results
                    output_file = f"filtered_{selected_field.replace(' ', '_').lower()}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(filtered_papers, f, indent=2, ensure_ascii=False)
                    print(f"💾 Filtered papers saved to: {output_file}")
                else:
                    print(f"❌ No papers found for field: {selected_field}")
            else:
                print("❌ Invalid choice. Please enter a number between 0-10.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
