import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_ranking_diagram():
    top_users = [{'nickname': 'Uchqun', 'points': 1500}, {'nickname': 'User2', 'points': 1200}, {'nickname': 'User3', 'points': 1000}, {'nickname': 'Hacker', 'points': 800}]
    
    if not top_users:
        return None
        
    names = [u['nickname'][:15] for u in top_users]
    points = [u['points'] for u in top_users]
    
    # Reverse to show highest at the top
    names = names[::-1]
    points = points[::-1]

    fig, ax = plt.subplots(figsize=(8, max(4, len(top_users) * 0.6)))
    
    # Set dark background
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    # Create horizontal bars
    bars = ax.barh(names, points, color='#ef4444', height=0.6, edgecolor='#b91c1c')
    
    # Add text labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(points)*0.02, bar.get_y() + bar.get_height()/2, 
                f'{int(width)} pts', 
                ha='left', va='center', color='white', fontweight='bold', fontsize=12)

    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#475569')
    
    ax.tick_params(axis='y', colors='white', labelsize=12)
    ax.tick_params(axis='x', colors='#94a3b8')
    
    plt.title("🏆 SPARK CTF SCOREBOARD", color='white', pad=20, fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("test_diagram.png", format='png', bbox_inches='tight', facecolor='#0f172a', dpi=200)
    print("Saved test_diagram.png")

create_ranking_diagram()
