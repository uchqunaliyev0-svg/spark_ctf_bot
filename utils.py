import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def generate_ranking_image(top_users):
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
    
    plt.title("SPARK CTF SCOREBOARD", color='white', pad=20, fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#0f172a', dpi=200)
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

import datetime
import matplotlib.dates as mdates

def generate_scoreboard_chart(top_users, solves):
    if not top_users or not solves:
        return None
    
    # Map user_id to nickname
    user_map = {u['user_id']: u['nickname'] for u in top_users}
    user_ids = [u['user_id'] for u in top_users]
    
    # Order for legend consistency
    user_ids = sorted(user_ids, key=lambda x: user_map[x])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    all_solved_times = [s['solved_at'] for s in solves]
    start_time = min(all_solved_times) - datetime.timedelta(minutes=30)
    end_time = datetime.datetime.now()
    
    for uid in user_ids:
        user_solves = [s for s in solves if s['user_id'] == uid]
        
        times = [start_time]
        scores = [0]
        current_score = 0
        
        for solve in user_solves:
            current_score += solve['points']
            times.append(solve['solved_at'])
            scores.append(current_score)
            
        times.append(end_time)
        scores.append(current_score)
        
        ax.step(times, scores, where='post', label=user_map[uid], linewidth=2)

    ax.set_title("SCORE PROGRESSION", color='white', pad=20, fontsize=16, fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.tick_params(axis='both', colors='white')
    ax.grid(True, linestyle='--', alpha=0.1)
    
    # Styling spines
    for spine in ax.spines.values():
        spine.set_color('#475569')
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, fontsize=9)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#0f172a', dpi=200)
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()
