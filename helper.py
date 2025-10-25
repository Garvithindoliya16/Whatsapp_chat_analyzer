from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import emoji
import pandas as pd
import tempfile
import seaborn as sns
import os
from fpdf import FPDF

extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    #Total Number of messages
    num_messages=df.shape

    #Total Number of Words
    words=[]
    for i in df['message']:
        words.extend(i.split())


    #Total Number of Mediamessages
    num_media_messages = df[df['message']=="<Media omitted>\n"].shape[0]

    #Total Number of Links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages[0],len(words),num_media_messages,len(links)

def most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count': 'Percent', 'user': 'Name'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopWords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stopWords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emojies_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojies=[]
    for i in df['message']:
        emojies.extend([c for c in i if emoji.is_emoji(c)])
    
    emoji_df = pd.DataFrame(Counter(emojies).most_common(len(Counter(emojies))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))

    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
    
def activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def generate_full_pdf(selected_user, df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ===== TITLE =====
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "WhatsApp Chat Analyzer Report", ln=True, align="C")
    pdf.ln(10)

    # ===== BASIC STATS =====
    num_messages, words, num_media_messages, num_links = fetch_stats(selected_user, df)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Analysis for: {selected_user}")
    pdf.multi_cell(0, 10, f"Total Messages: {num_messages}")
    pdf.multi_cell(0, 10, f"Total Words: {words}")
    pdf.multi_cell(0, 10, f"Media Shared: {num_media_messages}")
    pdf.multi_cell(0, 10, f"Links Shared: {num_links}")
    pdf.ln(5)

    # Temp files list for cleanup
    temp_files = []

    def add_plot_to_pdf(fig, title):
        """Helper function to save a matplotlib plot to temp and add to PDF."""
        tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(tmp_img.name, bbox_inches='tight')
        plt.close(fig)
        temp_files.append(tmp_img.name)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.image(tmp_img.name, x=10, y=30, w=180)

    # ===== MONTHLY TIMELINE =====
    timeline = monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='black')
    ax.set_facecolor("pink")
    plt.xlabel("Time")
    plt.ylabel("Messages")
    plt.xticks(rotation='vertical')
    add_plot_to_pdf(fig, "Monthly Timeline")

    # ===== DAILY TIMELINE =====
    dailyy_timeline = daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(dailyy_timeline['only_date'], dailyy_timeline['message'], color='blue')
    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.xticks(rotation=90)
    add_plot_to_pdf(fig, "Daily Timeline")

    # ===== ACTIVITY MAP =====
    daily_activity = activity(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(daily_activity.index, daily_activity.values, color='green')
    plt.xticks(rotation=45)
    add_plot_to_pdf(fig, "Most Busy Day")

    monthlyy_activity = monthly_activity(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(monthlyy_activity.index, monthlyy_activity.values, color='orange')
    plt.xticks(rotation=45)
    add_plot_to_pdf(fig, "Most Busy Month")

    # ===== HEATMAP =====
    user_heatmap = activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    sns.heatmap(user_heatmap, ax=ax)
    add_plot_to_pdf(fig, "Weekly Activity Heatmap")

    # ===== WORDCLOUD =====
    df_wc = create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    ax.axis("off")
    add_plot_to_pdf(fig, "Wordcloud")

    # ===== EMOJIS =====
    emojies_df =emojies_analysis(selected_user, df)
    if len(emojies_df) > 0:
        fig, ax = plt.subplots()
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        ax.pie(emojies_df[1].head(), labels=emojies_df[0].head(), autopct="%0.2f")
        add_plot_to_pdf(fig, "Top Emojis")

    # ===== SAVE PDF =====
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(pdf_file.name)

    # Clean up temp images
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

    return pdf_file.name
