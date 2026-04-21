import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_ranking_image():
    top_users = [{'nickname': 'Uchqun', 'points': 1500}, {'nickname': 'User2', 'points': 1200}, {'nickname': 'User3', 'points': 1000}, {'nickname': 'Hacker', 'points': 800}]
    fig, ax = plt.subplots(figsize=(8, len(top_users) * 0.5 + 2))
    ax.axis('tight')
    ax.axis('off')
    
    columns = ('RANK', 'NICKNAME', 'SCORE')
    cell_text = []
    for i, u in enumerate(top_users):
        cell_text.append([str(i+1), u['nickname'], str(u['points'])])
        
    table = ax.table(cellText=cell_text, colLabels=columns, loc='center', cellLoc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 2)
    
    for i in range(len(columns)):
        cell = table[0, i]
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#dc2626') # Red header for CTF feel
        cell.set_edgecolor('#991b1b')

    for r in range(1, len(top_users) + 1):
        for c in range(len(columns)):
            cell = table[r, c]
            cell.set_text_props(color='white')
            cell.set_facecolor('#171717' if r % 2 == 0 else '#262626')
            cell.set_edgecolor('#404040')
            if c == 1:
                cell._loc = 'left'

    fig.patch.set_facecolor('#0a0a0a')
    plt.title("SPARK CTF LEADERBOARD", color='#dc2626', pad=20, fontsize=18, weight='bold', fontfamily='monospace')
    
    plt.savefig("test_table.png", format='png', bbox_inches='tight', facecolor='#0a0a0a', dpi=200)
    print("Saved test_table.png")

create_ranking_image()
