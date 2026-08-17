"""
app.py
======
Interactive Streamlit Dashboard for Roblox Sentiment Analysis.
Features:
- Sentiment Overview
- Sentiment Analysis (Keywords, Wordclouds)
- Temporal Trend Analysis (Daily, Monthly, Peak Days)
- Model & Evaluation (SVM vs IndoBERT side-by-side)
- Scraping & Preprocessing Pipeline
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
import joblib
from typing import cast

# Try importing wordcloud
try:
    from wordcloud import WordCloud, STOPWORDS as WC_STOPWORDS
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Analisis Sentimen Roblox",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Growlytics-inspired Modern Design)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Overall page font & background */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Navigation radio sidebar */
    div[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem !important;
    }
    
    /* Hide the radio button circles in the sidebar for a navigation look */
    div[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 14px !important;
        color: #475569 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        display: block;
        margin-bottom: 2px;
        width: 100%;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #F1F5F9;
        color: #0F172A !important;
        border-color: #CBD5E1;
    }
    
    /* Remove radio dot circle */
    div[data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stWidgetLabel"] {
        margin-left: 0 !important;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] label input[type="radio"] {
        display: none;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
        border-color: #818CF8 !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Custom cards styling */
    .glass-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 24px !important;
    }
    
    /* Custom metric card */
    .custom-metric {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        gap: 6px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .custom-metric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    .custom-metric-label {
        font-size: 11px;
        color: #64748B;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .custom-metric-value {
        font-size: 28px;
        color: #0F172A;
        font-weight: 700;
        line-height: 1.1;
    }
    .custom-metric-delta {
        font-size: 11px;
        font-weight: 600;
        margin-top: 4px;
    }
    .delta-positive { color: #10B981; }
    .delta-negative { color: #EF4444; }
    .delta-neutral { color: #64748B; }
    
    /* Styled headings */
    h1 {
        font-size: 28px !important;
        margin-bottom: 20px !important;
        padding-bottom: 10px !important;
        border-bottom: 1px solid #E2E8F0 !important;
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    h2 {
        font-size: 18px !important;
        border-left: 4px solid #6366F1 !important;
        padding-left: 12px !important;
        margin-top: 24px !important;
        margin-bottom: 16px !important;
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    h3 {
        font-size: 15px !important;
        color: #334155 !important;
        margin-top: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Info/Success box overrides */
    div.stAlert {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02) !important;
    }
    
    /* Tables styling */
    div[data-testid="stTable"] table {
        border-collapse: collapse !important;
        width: 100% !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    div[data-testid="stTable"] th {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }
    
    div[data-testid="stTable"] td {
        padding: 14px 16px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        color: #334155 !important;
        font-size: 13px !important;
    }
    
    /* Native metric cards override */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    
    div[data-testid="stMetric"] label {
        font-size: 11px !important;
        color: #64748B !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        color: #0F172A !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper to draw a custom card metric
def draw_metric_card(icon: str, label: str, value: str, delta: str | None = None, delta_type: str = "positive"):
    delta_html = ""
    if delta:
        if delta_type == "positive":
            delta_html = f'<div class="custom-metric-delta delta-positive">▲ {delta}</div>'
        elif delta_type == "negative":
            delta_html = f'<div class="custom-metric-delta delta-negative">▼ {delta}</div>'
            
    st.markdown(f"""
        <div class="custom-metric">
            <div class="custom-metric-label">
                <span>{icon}</span> {label}
            </div>
            <div class="custom-metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


# Cache data loading
@st.cache_data
def load_dataset():
    path = "data/processed/roblox_sentiment.csv"
    if not os.path.exists(path):
        # Fallback to teacher pseudo label file
        path = "data/processed/roblox_with_teacher_pseudo_label.csv"
        if not os.path.exists(path):
            return pd.DataFrame()
            
    df = pd.read_csv(path)
    
    # Make sure we have proper datetime column
    if 'at' in df.columns:
        df['at'] = pd.to_datetime(df['at'])
    else:
        # Create dummy dates if not exists
        df['at'] = pd.date_range(start="2026-02-25", periods=len(df), freq='min')
        
    # Helper to map numerical score to rating label
    if 'score' in df.columns:
        def score_to_sent(score):
            if score in [1, 2]: return 'negatif'
            elif score == 3: return 'netral'
            else: return 'positif'
        df['sentiment_rating'] = df['score'].apply(score_to_sent)
    else:
        df['sentiment_rating'] = 'netral'
        
    # Normalize teacher label column if sentiment_indobert is not in columns
    if 'sentiment_indobert' in df.columns:
        df['sentiment_indobert'] = df['sentiment_indobert'].str.strip().str.lower()
    elif 'pseudo_label_teacher' in df.columns:
        df['sentiment_indobert'] = df['pseudo_label_teacher'].str.strip().str.lower()
    else:
        df['sentiment_indobert'] = 'netral'
        
    return df

df_display = load_dataset()

# Helper for plotly formatting
def apply_plotly_style(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=11, color="#4a5568"),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#edf2f7")
    fig.update_yaxes(showgrid=True, gridcolor="#edf2f7")
    return fig

# Helper for keyword extraction
# Partikel/klitik yang lolos stopword removal NLTK tapi gak bawa makna topik
# sendiri (mis. "nya" posesif: "game nya", "chat nya") - dibuang khusus buat
# tampilan kata kunci/topik/wordcloud, TIDAK menyentuh cleaned_content asli
# yang dipakai training SVM (biar gak perlu retrain ulang).
DISPLAY_NOISE_WORDS = {"nya"}


def is_display_noise(tok: str) -> bool:
    # "_neg" adalah marker internal negation-handling dari src/preprocessor.py
    # (mis. "gak bisa" -> "bisa_neg"), bukan kata asli - jangan ditampilkan ke user.
    return tok in DISPLAY_NOISE_WORDS or tok.endswith("_neg")

def extract_top_keywords(texts, n=1, top_k=10):
    from collections import Counter
    words = []
    for t in texts:
        if not isinstance(t, str):
            continue
        tokens = [tok for tok in t.split() if not is_display_noise(tok)]
        if n == 1:
            words.extend(tokens)
        else:
            # build n-grams
            for i in range(len(tokens) - n + 1):
                words.append(" ".join(tokens[i:i+n]))

    # Filter short tokens
    words = [w for w in words if len(w.replace(" ", "")) > 2]

    counter = Counter(words)
    return counter.most_common(top_k)

def build_wordcloud_frequencies(texts, top_n=50):
    from collections import Counter
    words = []
    for t in texts:
        if not isinstance(t, str):
            continue
        words.extend([w for w in t.split() if len(w) > 2 and not is_display_noise(w)])
    counter = Counter(words)
    return counter.most_common(top_n)

def render_wordcloud_plotly(frequencies, title, color_scale="Greens"):
    if not frequencies:
        fig = px.scatter()
        fig.update_layout(title="Tidak ada kata")
        return fig
    
    words = [w[0] for w in frequencies]
    counts = [w[1] for w in frequencies]
    
    # Generate random layout positions for word cloud representation
    np.random.seed(42)
    x = np.random.uniform(-10, 10, len(words))
    y = np.random.uniform(-10, 10, len(words))
    
    fig = px.scatter(
        x=x, y=y, text=words, size=counts, color=counts,
        color_continuous_scale=color_scale,
        size_max=35
    )
    fig.update_traces(textposition='middle center', mode='text')
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_layout(coloraxis_showscale=False)
    return fig

def render_wordcloud_native(texts, title, colormap="Greens"):
    if not WORDCLOUD_AVAILABLE:
        # Fallback to plotly scatter cloud
        freqs = build_wordcloud_frequencies(texts, top_n=40)
        return st.plotly_chart(apply_plotly_style(render_wordcloud_plotly(freqs, title, colormap)), use_container_width=True)
        
    text_content = " ".join([t for t in texts if isinstance(t, str) and len(t) > 2])
    if not text_content.strip():
        st.info("Data teks tidak mencukupi untuk menghasilkan Awan Kata.")
        return
        
    try:
        # Create WordCloud object
        wc = WordCloud(
            background_color='white',
            width=800,
            height=400,
            colormap=colormap,
            max_words=60,
            stopwords=WC_STOPWORDS
        )
        wc.generate(text_content)
        
        # Display image directly in Streamlit
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.error(f"Gagal memuat visualisasi Word Cloud: {e}")

def get_mismatch_analysis(df):
    # Find mismatch cases
    mismatch_df = df[df['sentiment_rating'] != df['sentiment_indobert']]
    
    # Classify mismatch types
    def classify_mismatch(row):
        rat = row['sentiment_rating'].capitalize()
        txt = row['sentiment_indobert'].capitalize()
        return f"{rat} Rating → {txt} Teks"
        
    mismatch_df['type'] = mismatch_df.apply(classify_mismatch, axis=1)
    return mismatch_df['type'].value_counts()

def get_top_representative_reviews(df, sentiment, keywords, bigrams, limit=3):
    # Filter sentiment
    sub_df = df[df['sentiment_indobert'] == sentiment]
    
    # Find reviews containing any of the top bigrams or keywords
    scored_reviews = []
    for idx, row in sub_df.iterrows():
        # buang noise words/marker _neg juga di sini, konsisten sama cara bigrams/keywords
        # dibangun di extract_top_keywords() - kalau enggak, "chat bagus" (bigram
        # tanpa "nya") gak bakal ketemu di teks asli yang masih "chat nya bagus"
        raw_tokens = str(row.get('cleaned_content', '')).split()
        text = " ".join(tok for tok in raw_tokens if not is_display_noise(tok))
        orig_text = str(row.get('content', ''))
        score = 0
        topic = "Lainnya"
        
        # Check bigrams first (higher weight)
        for bg, freq in bigrams[:5]:
            if bg in text:
                score += 5
                topic = bg.capitalize()
                
        # Check keywords
        for kw, freq in keywords[:5]:
            if kw in text:
                score += 2
                if topic == "Lainnya":
                    topic = kw.capitalize()
                    
        if score > 0 and len(orig_text.split()) > 4: # Prefer descriptive text
            scored_reviews.append({
                "content": orig_text,
                "score": score,
                "primary_topic": topic
            })
            
    if not scored_reviews:
        return pd.DataFrame(columns=["content", "primary_topic"])
        
    res_df = pd.DataFrame(scored_reviews).sort_values('score', ascending=False)
    return res_df.drop_duplicates(subset=['content']).head(limit)


# Sidebar Menu
with st.sidebar:
    col_logo, col_title = st.columns([1, 3])
    with col_logo:
        st.image("reports/figures/roblox_logo_sidebar.png", width=50)
    with col_title:
        st.markdown("<h3 style='margin:0; padding-top:4px; font-size: 15px; font-weight:700;'>Roblox Review</h3>", unsafe_allow_html=True)
        st.markdown("<span style='font-size: 11px; color: #64748B; font-weight:500;'>Sentimen & Tren</span>", unsafe_allow_html=True)
    
    st.write("") # Spacing
    st.markdown("<p style='font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;'>MENU UTAMA</p>", unsafe_allow_html=True)
    
    page = st.radio(
        "Pilih Halaman:",
        ["📈 Ringkasan Eksekutif", "📊 Analisis Sentimen Teks", "📉 Tren Temporal", "🔬 Model & Evaluasi", "⚙️ Pipeline Praproses"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<div class='glass-card' style='padding: 15px;'>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; font-weight:700; font-size:12px; color: #1E293B;'>Fokus Analisis</p>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; font-size:11px; color:#64748B; line-height: 1.4;'>Analisis temporal dan pemodelan sentimen berbasis teks secara objektif.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main App Navigation Router

if page == "📈 Ringkasan Eksekutif":
    st.title("Ringkasan Eksekutif Analisis Sentimen")
    
    # Calculate stats
    sentiment_counts = df_display['sentiment_indobert'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    total_reviews = len(df_display)
    pct_pos = (df_display['sentiment_indobert'] == 'positif').mean() * 100
    pct_neg = (df_display['sentiment_indobert'] == 'negatif').mean() * 100
    avg_rating = df_display['score'].mean() if 'score' in df_display.columns else 0.0
    
    # Load model metrics
    indo_model_metrics = None
    metrics_file_path = "models/indobert_sentiment/metrics_indobert.json"
    if os.path.exists(metrics_file_path):
        with open(metrics_file_path, 'r', encoding='utf-8') as f:
            indo_model_metrics = json.load(f)
    acc_indo = indo_model_metrics['test_accuracy'] * 100 if indo_model_metrics else 0.0
    agreement_rate = (df_display['sentiment_rating'] == df_display['sentiment_indobert']).mean() * 100
    
    # Extract month with highest volume
    df_display['month'] = df_display['at'].dt.strftime('%B %Y')  # type: ignore
    monthly_volume = df_display['month'].value_counts().reset_index()
    highest_month = monthly_volume['month'].iloc[0] if not monthly_volume.empty else "—"
    dominant_sentiment = "Positif" if pct_pos > pct_neg else "Negatif"
    
    # Metrics display row (3x2 Layout to prevent cut-offs)
    col1, col2, col3 = st.columns(3)
    with col1:
        draw_metric_card("📂", "Total Ulasan", f"{total_reviews:,}", "Seluruh periode", "neutral")
        st.write("")
        draw_metric_card("🟢", "Sentimen Positif", f"{pct_pos:.1f}%", f"{(df_display['sentiment_indobert'] == 'positif').sum():,} ulasan", "positive")
    with col2:
        draw_metric_card("⭐", "Rating Rata-rata", f"{avg_rating:.2f} / 5.0", "Skala 1-5 bintang", "neutral")
        st.write("")
        draw_metric_card("🔴", "Sentimen Negatif", f"{pct_neg:.1f}%", f"{(df_display['sentiment_indobert'] == 'negatif').sum():,} ulasan", "negative")
    with col3:
        draw_metric_card("🤝", "Agreement Rate", f"{agreement_rate:.2f}%", "Kesesuaian rating & teks", "positive")
        st.write("")
        draw_metric_card("🧠", "Accuracy IndoBERT", f"{acc_indo:.2f}%", "Model utama student", "positive")
        
    st.write("") # Spacing
    
    # Donut Chart
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Distribusi Sentimen Ulasan Pengguna")
    fig_pie = px.pie(
        sentiment_counts, values='count', names='sentiment',
        color='sentiment',
        color_discrete_map={'positif': '#10B981', 'netral': '#F59E0B', 'negatif': '#EF4444'},
        hole=0.6
    )
    fig_pie.update_traces(
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    st.plotly_chart(apply_plotly_style(fig_pie), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Key findings
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Ringkasan Eksekutif Temuan Penelitian")
    st.markdown(
        f"""
1. **Dimensi Dataset:** Total ulasan yang dianalisis adalah sebanyak **{total_reviews:,}** ulasan pengguna dari Google Play Store selama periode Februari hingga April 2026.
2. **Polaritas Sentimen Dominan:** Hasil klasifikasi model utama menunjukkan bahwa sentimen didominasi oleh kelas **{dominant_sentiment}** dengan proporsi **{pct_pos:.1f}%** ulasan positif dan **{pct_neg:.1f}%** ulasan negatif.
3. **Akurasi Model Utama:** Model IndoBERT hasil fine-tuning berhasil mencapai akurasi sebesar **{acc_indo:.2f}%** pada data uji.
4. **Tingkat Keselarasan (Agreement Rate):** Tingkat kesesuaian antara rating bintang pengguna dan polaritas teks ulasan adalah sebesar **{agreement_rate:.2f}%**.
5. **Aktivitas Ulasan Tertinggi:** Volume aktivitas ulasan pengguna mencapai puncak tertingginya pada bulan **{highest_month}**.
        """.strip()
    )
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📊 Analisis Sentimen Teks":
    st.title("Analisis Semantik Teks Ulasan")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Proporsi Polaritas Sentimen")
    sentiment_counts = df_display['sentiment_indobert'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    fig_sent = px.pie(
        sentiment_counts, values='count', names='sentiment',
        color='sentiment',
        color_discrete_map={'positif': '#10B981', 'netral': '#F59E0B', 'negatif': '#EF4444'},
        hole=0.4
    )
    fig_sent.update_traces(
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    st.plotly_chart(apply_plotly_style(fig_sent), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Extract keywords
    pos_texts = df_display[df_display['sentiment_indobert'] == 'positif']['cleaned_content'].fillna("").astype(str).tolist()
    neg_texts = df_display[df_display['sentiment_indobert'] == 'negatif']['cleaned_content'].fillna("").astype(str).tolist()
    pos_keywords = extract_top_keywords(pos_texts, n=1, top_k=10)
    neg_keywords = extract_top_keywords(neg_texts, n=1, top_k=10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Top 10 Kata Kunci Positif")
        df_pos_kw = pd.DataFrame(pos_keywords, columns=["Kata", "Frekuensi"])
        fig_pos_kw = px.bar(df_pos_kw, x="Frekuensi", y="Kata", orientation="h", color_discrete_sequence=["#10B981"])
        st.plotly_chart(apply_plotly_style(fig_pos_kw), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Top 10 Kata Kunci Negatif")
        df_neg_kw = pd.DataFrame(neg_keywords, columns=["Kata", "Frekuensi"])
        fig_neg_kw = px.bar(df_neg_kw, x="Frekuensi", y="Kata", orientation="h", color_discrete_sequence=["#EF4444"])
        st.plotly_chart(apply_plotly_style(fig_neg_kw), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Word Clouds
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Awan Kata (Word Cloud)")
    wc_col1, wc_col2 = st.columns(2)
    with wc_col1:
        st.markdown("**Ulasan Positif**")
        render_wordcloud_native(pos_texts, "Positif", "Greens")
    with wc_col2:
        st.markdown("**Ulasan Negatif**")
        render_wordcloud_native(neg_texts, "Negatif", "Reds")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📉 Tren Temporal":
    st.title("Analisis Tren Temporal Review Roblox")
    
    sentiment_source_col = "sentiment_indobert"
    label_ui = {'positif': 'Positif', 'netral': 'Netral', 'negatif': 'Negatif'}
    
    df_tmp2 = df_display.copy()
    df_tmp2 = df_tmp2.dropna(subset=['at'])
    df_tmp2[sentiment_source_col] = df_tmp2[sentiment_source_col].astype(str).str.strip().str.lower()
    df_tmp2 = df_tmp2[df_tmp2[sentiment_source_col].isin(['positif', 'netral', 'negatif'])]
    df_tmp2['sentiment_ui_ts'] = df_tmp2[sentiment_source_col].map(label_ui)
    df_tmp2['date'] = df_tmp2['at'].dt.date
    
    # Tren Harian
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("A. Tren Sentimen Harian")
    st.markdown("Visualisasi menunjukkan perkembangan volume ulasan harian berdasarkan polaritas sentimen.")
    trend_df = df_tmp2.groupby(['date', 'sentiment_ui_ts']).size().reset_index(name='count')
    fig_line = px.line(
        trend_df, x='date', y='count', color='sentiment_ui_ts',
        color_discrete_map={'Positif': '#10B981', 'Netral': '#F59E0B', 'Negatif': '#EF4444'},
        line_shape='spline'
    )
    fig_line.update_layout(xaxis_title="Tanggal", yaxis_title="Jumlah Review")
    fig_line.update_layout(legend_title_text="Sentimen")
    st.plotly_chart(apply_plotly_style(fig_line), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Hari dengan Volume Review Tertinggi
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("B. Analisis Deviasi Volume Ulasan Terbanyak")
    st.markdown("Tabel berikut menyajikan sepuluh tanggal dengan akumulasi volume ulasan tertinggi selama periode penelitian.")
    daily_counts = df_tmp2.groupby(['date']).size().reset_index(name='Total Review')
    top_10_days = daily_counts.sort_values('Total Review', ascending=False).head(10).reset_index(drop=True)
    top_10_days.index += 1
    st.dataframe(top_10_days, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Metodologi Analisis Fluktuasi
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("💡 Metodologi Analisis Fluktuasi Harian")
    st.markdown("Pendekatan sistematis yang digunakan peneliti untuk mengidentifikasi faktor di balik anomali volume ulasan:")
    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.markdown("""
        <div style="border:1px solid #e2e8f0; border-radius:12px; padding:15px; background-color:#e8f5e9; height:100%;">
            <h5 style="color:#2e7d32; margin-top:0;">1. Deteksi Anomali Volumetrik</h5>
            <p style="color:#2e7d32; font-size:12px; margin-bottom:0;">
                Menghitung volume ulasan harian untuk mendeteksi deviasi ekstrem (lonjakan tajam) di luar rata-rata volume harian normal.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_met2:
        st.markdown("""
        <div style="border:1px solid #e2e8f0; border-radius:12px; padding:15px; background-color:#e3f2fd; height:100%;">
            <h5 style="color:#1565c0; margin-top:0;">2. Ekstraksi Kata Kunci & Bigram</h5>
            <p style="color:#1565c0; font-size:12px; margin-bottom:0;">
                Mengekstrak kata kunci dominan dan bigram (2-kata berdampingan) pada tanggal puncak untuk mengisolasi topik utama keluhan pengguna.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_met3:
        st.markdown("""
        <div style="border:1px solid #e2e8f0; border-radius:12px; padding:15px; background-color:#fff3e0; height:100%;">
            <h5 style="color:#e65100; margin-top:0;">3. Triangulasi Peristiwa Riil</h5>
            <p style="color:#e65100; font-size:12px; margin-bottom:0;">
                Mencocokkan temuan teks ulasan dengan log gangguan server resmi dan pembaruan sistem Roblox untuk memvalidasi keluhan nyata pengguna.
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.info("Kombinasi metode di atas menunjukkan secara empiris bahwa ulasan Google Play Store bukan sekadar rating acak, melainkan representasi langsung dari kestabilan ekosistem aplikasi pada tanggal tersebut.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analisis Topik Dominan
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("C. Analisis Faktor dan Topik Dominan pada Hari Puncak")
    
    def _peak_count(date_str):
        d = pd.to_datetime(date_str).date()
        row = top_10_days[top_10_days['date'] == d]
        return f"{int(row['Total Review'].iloc[0]):,}".replace(",", ".") if not row.empty else "-"

    top_3_dates = top_10_days['date'].head(3).tolist()

    # Narasi per tanggal puncak diverifikasi manual terhadap teks ulasan asli + sumber eksternal
    # (lihat Tabel 4.14). Tanggal di luar daftar ini otomatis dapat fallback jujur, bukan diklaim.
    first_day = df_tmp2['date'].min()
    verified_peak_notes = {
        pd.to_datetime('2026-04-09').date(): (
            "berkaitan dengan kontroversi kebijakan verifikasi umur untuk mengakses fitur chat "
            "(berlaku global sejak 7 Januari 2026); 35 dari 361 ulasan berperingkat rendah (rating ≤2) "
            "pada tanggal ini eksplisit menyebut istilah \"verifikasi\", \"umur\", atau \"dibatasi\""
        ),
        pd.to_datetime('2026-04-21').date(): (
            "dari 404 ulasan berperingkat rendah (rating ≤2) pada tanggal ini, didominasi kata kunci "
            "\"update\" (111 kemunculan); istilah login/server muncul namun dengan frekuensi rendah "
            "(4 dan 3 kemunculan) sehingga bukan tema dominan"
        ),
    }

    peak_lines = []
    for i, peak_date in enumerate(top_3_dates, start=1):
        count_str = _peak_count(str(peak_date))
        if peak_date == first_day:
            note = "merupakan hari pertama periode pengambilan data, sehingga lonjakan volume kemungkinan besar artefak batas awal scraping, bukan cerminan aktivitas pengguna riil"
        elif peak_date in verified_peak_notes:
            note = verified_peak_notes[peak_date]
        else:
            note = "faktor spesifik pada tanggal ini belum diverifikasi terhadap sumber eksternal — lihat kata kunci dominan pada bagian di bawah"
        peak_lines.append(f"{i}. **{peak_date.strftime('%d %B %Y')}** ({count_str} ulasan): {note}.")

    st.info(
        "**💡 Analisis Kata Kunci pada Hari Puncak Ulasan**\n\n"
        "Berdasarkan analisis frekuensi kata dan bigram pada hari-hari dengan volume ulasan tertinggi, "
        "tiga tanggal puncak pada periode penelitian ini menunjukkan pola berikut:\n\n"
        + "\n".join(peak_lines)
    )

    for peak_date in top_3_dates:
        st.markdown(f"### Tanggal: {peak_date}")
        day_df = df_tmp2[df_tmp2['date'] == peak_date]
        
        # Sentiment distribution
        sent_dist = day_df.groupby('sentiment_ui_ts').size().reset_index(name='count')
        col1, col2 = st.columns([1,2])
        with col1:
            st.write("Distribusi Sentimen:")
            st.dataframe(sent_dist, use_container_width=True)
        with col2:
            fig_sent_pie = px.pie(
                sent_dist, values='count', names='sentiment_ui_ts', 
                color='sentiment_ui_ts',
                color_discrete_map={'Positif': '#10B981', 'Netral': '#F59E0B', 'Negatif': '#EF4444'},
                hole=0.4
            )
            fig_sent_pie.update_traces(
                textinfo='percent+label',
                hoverinfo='label+value+percent',
                marker=dict(line=dict(color='#ffffff', width=2))
            )
            st.plotly_chart(apply_plotly_style(fig_sent_pie), use_container_width=True)
        
        # Keywords and bigrams
        pos_texts_day = day_df[day_df[sentiment_source_col] == 'positif']['cleaned_content'].fillna("").astype(str).tolist()
        neg_texts_day = day_df[day_df[sentiment_source_col] == 'negatif']['cleaned_content'].fillna("").astype(str).tolist()
        pos_kw_day = extract_top_keywords(pos_texts_day, n=1, top_k=5)
        neg_kw_day = extract_top_keywords(neg_texts_day, n=1, top_k=5)
        pos_bg_day = extract_top_keywords(pos_texts_day, n=2, top_k=5)
        neg_bg_day = extract_top_keywords(neg_texts_day, n=2, top_k=5)
        
        kw_col1, kw_col2, kw_col3, kw_col4 = st.columns(4)
        with kw_col1:
            st.write("Kata Kunci Positif:")
            df_pkw = pd.DataFrame(pos_kw_day, columns=["Kata", "Frekuensi"])
            st.dataframe(df_pkw, use_container_width=True, hide_index=True)
        with kw_col2:
            st.write("Kata Kunci Negatif:")
            df_nkw = pd.DataFrame(neg_kw_day, columns=["Kata", "Frekuensi"])
            st.dataframe(df_nkw, use_container_width=True, hide_index=True)
        with kw_col3:
            st.write("Bigram Positif:")
            df_pbg = pd.DataFrame(pos_bg_day, columns=["Frasa", "Frekuensi"])
            st.dataframe(df_pbg, use_container_width=True, hide_index=True)
        with kw_col4:
            st.write("Bigram Negatif:")
            df_nbg = pd.DataFrame(neg_bg_day, columns=["Frasa", "Frekuensi"])
            st.dataframe(df_nbg, use_container_width=True, hide_index=True)
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Review Representatif
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("D. Sampel Ulasan Representatif pada Hari Puncak")
    for peak_date in top_3_dates:
        st.markdown(f"### Tanggal: {peak_date}")
        day_df = df_tmp2[df_tmp2['date'] == peak_date]
        pos_texts_day = day_df[day_df[sentiment_source_col] == 'positif']['cleaned_content'].fillna("").astype(str).tolist()
        neg_texts_day = day_df[day_df[sentiment_source_col] == 'negatif']['cleaned_content'].fillna("").astype(str).tolist()
        pos_kw_day = extract_top_keywords(pos_texts_day, n=1, top_k=5)
        neg_kw_day = extract_top_keywords(neg_texts_day, n=1, top_k=5)
        pos_bg_day = extract_top_keywords(pos_texts_day, n=2, top_k=5)
        neg_bg_day = extract_top_keywords(neg_texts_day, n=2, top_k=5)
        
        all_keywords = pos_kw_day + neg_kw_day
        topic_counts = {}
        for kw, _ in all_keywords:
            topic_mapping = {
                "chat": "Fitur Chat", "lag": "Bug dan Performa", "bug": "Bug dan Performa",
                "disconnect": "Bug dan Performa", "game": "Pengalaman Bermain", "seru": "Pengalaman Bermain",
                "map": "Variasi Game/Map", "update": "Update Aplikasi", "akun": "Akun & Keamanan", "avatar": "Avatar/Fitur"
            }
            if kw in topic_mapping:
                topic = topic_mapping[kw]
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
                
        st.markdown("#### Topik Utama Terdeteksi:")
        if topic_counts:
            top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            for topic, cnt in top_topics:
                st.markdown(f"- {topic}")
        else:
            st.markdown("- Topik tidak terdeteksi")
            
        pos_rep_day = get_top_representative_reviews(day_df, 'positif', pos_kw_day, pos_bg_day, limit=2)
        neg_rep_day = get_top_representative_reviews(day_df, 'negatif', neg_kw_day, neg_bg_day, limit=2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Ulasan Positif:")
            if not pos_rep_day.empty:
                for idx, row in pos_rep_day.iterrows():
                    st.markdown(f"""
                    <div style="border:1px solid #c8e6c9; padding:12px; border-radius:8px; margin:8px 0; background-color:#e8f5e9;">
                        <b>Topik:</b> {row['primary_topic']}<br><b>Ulasan:</b> "{row['content']}"
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("Ulasan informatif tidak ditemukan.")
        with col2:
            st.markdown("#### Ulasan Negatif:")
            if not neg_rep_day.empty:
                for idx, row in neg_rep_day.iterrows():
                    st.markdown(f"""
                    <div style="border:1px solid #ffcdd2; padding:12px; border-radius:8px; margin:8px 0; background-color:#ffebee;">
                        <b>Topik:</b> {row['primary_topic']}<br><b>Ulasan:</b> "{row['content']}"
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("Ulasan informatif tidak ditemukan.")
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # E. Klasifikasi Faktor Dominan
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("E. Klasifikasi Faktor Dominan Keluhan Pengguna")
    
    all_pos_texts = df_tmp2[df_tmp2[sentiment_source_col] == 'positif']['cleaned_content'].fillna("").astype(str).tolist()
    all_neg_texts = df_tmp2[df_tmp2[sentiment_source_col] == 'negatif']['cleaned_content'].fillna("").astype(str).tolist()
    all_pos_kw = extract_top_keywords(all_pos_texts, n=1, top_k=15)
    all_neg_kw = extract_top_keywords(all_neg_texts, n=1, top_k=15)
    
    st.markdown("""
    Berdasarkan hasil penapisan frekuensi kata kunci, frasa dua kata (bigram), dan ulasan representatif yang diekstrak, topik utama pembahasan pengguna terkonsentrasi pada beberapa dimensi berikut:
    - **Dimensi Kendala Teknis:** Masalah latensi permainan (lag), kegagalan konektivitas server (disconnect), dan kegagalan muat aset permainan (bug grafis).
    - **Dimensi Layanan Komunikasi:** Masalah kebijakan pembatasan fitur percakapan (fitur chat).
    - **Dimensi Pengalaman Pengguna (UX):** Kesenangan bermain, daya tarik visual, dan kemudahan interaksi antar-pemain.
    - **Dimensi Variasi Konten:** Ketersediaan variasi peta (map) dan permainan buatan komunitas.
    - **Dimensi Pembaruan Sistem:** Kebijakan dynamic heads dan proses verifikasi usia pengguna.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Kata Kunci Positif Dominan")
        df_all_pos_kw = pd.DataFrame(all_pos_kw, columns=["Kata", "Frekuensi"])
        fig_all_pos_kw = px.bar(df_all_pos_kw, x="Frekuensi", y="Kata", orientation="h", color_discrete_sequence=["#10B981"])
        st.plotly_chart(apply_plotly_style(fig_all_pos_kw), use_container_width=True)
    with col2:
        st.markdown("#### Kata Kunci Negatif Dominan")
        df_all_neg_kw = pd.DataFrame(all_neg_kw, columns=["Kata", "Frekuensi"])
        fig_all_neg_kw = px.bar(df_all_neg_kw, x="Frekuensi", y="Kata", orientation="h", color_discrete_sequence=["#EF4444"])
        st.plotly_chart(apply_plotly_style(fig_all_neg_kw), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # F. Kesimpulan Analisis Tren Temporal
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("F. Kesimpulan Analisis Tren Temporal")
    monthly_counts = df_tmp2.groupby(df_tmp2['at'].dt.strftime('%B %Y')).size()
    max_month = monthly_counts.idxmax()
    top_neg_word, top_neg_count = all_neg_kw[0] if all_neg_kw else ("-", 0)
    top_pos_word, top_pos_count = all_pos_kw[0] if all_pos_kw else ("-", 0)

    st.markdown(f"""
    * Puncak aktivitas ulasan bulanan terdeteksi pada periode **{max_month}**.
    * Kata kunci paling dominan pada ulasan bersentimen positif adalah **"{top_pos_word}"** ({top_pos_count} kemunculan).
    * Kata kunci paling dominan pada ulasan bersentimen negatif adalah **"{top_neg_word}"** ({top_neg_count} kemunculan).
    * Sebagian lonjakan ulasan negatif menunjukkan keterkaitan dengan peristiwa atau kebijakan produk riil (lihat Bagian C), namun tidak seluruh lonjakan dapat dikaitkan dengan insiden teknis spesifik — sebagian bersifat artefak metodologis pengumpulan data.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🔬 Model & Evaluasi":
    st.title("Evaluasi Model")
    
    # Pendekatan Hybrid
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Pendekatan Metodologi Perbandingan")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="border:1px solid #e2e8f0; border-radius:15px; padding:20px; background-color:#f8f9fa;">
            <h4 style="color:#1a2744; margin-top:0;">SVM + TF-IDF (Baseline)</h4>
            <p style="color:#4a5568; margin-bottom:5px;"><strong>Spesifikasi Metodologis:</strong></p>
            <ul style="color:#4a5568; padding-left:20px; margin-top:0;">
                <li>Algoritma machine learning klasik linear kernel.</li>
                <li>Ekstraksi fitur berbasis frekuensi kata (Bag-of-Words).</li>
                <li>Menggunakan representasi pembobotan nilai TF-IDF.</li>
                <li>Berperan sebagai baseline pembanding model transformer.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="border:1px solid #e2e8f0; border-radius:15px; padding:20px; background-color:#f8f9fa;">
            <h4 style="color:#1a2744; margin-top:0;">IndoBERT (Model Utama)</h4>
            <p style="color:#4a5568; margin-bottom:5px;"><strong>Spesifikasi Metodologis:</strong></p>
            <ul style="color:#4a5568; padding-left:20px; margin-top:0;">
                <li>Arsitektur Deep Learning berbasis Bidirectional Transformer.</li>
                <li>Memahami representasi semantik kontekstual teks ulasan.</li>
                <li>Di-fine-tune khusus pada dataset berbahasa Indonesia.</li>
                <li>Menjadi model klasifikasi utama untuk analisis data.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if 'label_source' in df_display.columns:
        _src_pct = (df_display['label_source'].value_counts(normalize=True) * 100)
        _pct_roberta = f"{_src_pct.get('roberta', 0):.1f}".replace(".", ",")
        _pct_manual = f"{_src_pct.get('manual', 0):.1f}".replace(".", ",")
    else:
        _pct_roberta, _pct_manual = "-", "-"
    st.info(f"Untuk membandingkan performa model secara adil (apple-to-apple), kedua model dilatih dan diuji menggunakan split data yang identik (random_state sama), dengan target label_final hasil gabungan pseudo-label RoBERTa ({_pct_roberta}%) dan label manual peneliti ({_pct_manual}%, tervalidasi Cochran). Kedua model juga memakai teknik penyeimbangan kelas yang setara (SVM: class_weight='balanced'; IndoBERT: weighted CrossEntropyLoss) agar perbandingan tidak bias oleh distribusi kelas netral yang minoritas.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Perbandingan Performa
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("A. Perbandingan Performa Model (SVM vs IndoBERT)")
    st.markdown("Tabel evaluasi menyajikan metrik performa objektif yang diuji pada dataset pengujian yang identik.")
    
    # Load IndoBERT metrics
    indo_model_metrics = None
    metrics_file_path = "models/indobert_sentiment/metrics_indobert.json"
    if os.path.exists(metrics_file_path):
        with open(metrics_file_path, 'r', encoding='utf-8') as f:
            indo_model_metrics = json.load(f)
            
    # Load SVM metrics
    svm_model_metrics = None
    svm_metrics_path = "models/svm_teacher/metrics_svm_teacher.json"
    if os.path.exists(svm_metrics_path):
        with open(svm_metrics_path, 'r', encoding='utf-8') as f:
            svm_model_metrics = json.load(f)
            
    col_perf1, col_perf2 = st.columns(2)
    with col_perf1:
        st.markdown("<h4 style='color:#1a2744; text-align:center; margin-bottom:15px;'>SVM Baseline (Baru)</h4>", unsafe_allow_html=True)
        if svm_model_metrics:
            acc_val = svm_model_metrics.get('test_accuracy', 0)
            prec_val = svm_model_metrics.get('precision_macro', 0)
            rec_val = svm_model_metrics.get('recall_macro', 0)
            f1_val = svm_model_metrics.get('f1_macro', 0)
            
            c_row1_col1, c_row1_col2 = st.columns(2)
            c_row2_col1, c_row2_col2 = st.columns(2)
            
            c_row1_col1.metric("Accuracy", f"{acc_val*100:.2f}%")
            c_row1_col2.metric("Precision", f"{prec_val*100:.2f}%")
            c_row2_col1.metric("Recall", f"{rec_val*100:.2f}%")
            c_row2_col2.metric("F1 Score", f"{f1_val*100:.2f}%")
        else:
            st.error("Metrik SVM tidak ditemukan!")
    with col_perf2:
        st.markdown("<h4 style='color:#1a2744; text-align:center; margin-bottom:15px;'>IndoBERT Fine-tuned</h4>", unsafe_allow_html=True)
        if indo_model_metrics:
            acc_val_indo = indo_model_metrics.get('test_accuracy', 0)
            prec_val_indo = indo_model_metrics.get('precision_macro', 0)
            rec_val_indo = indo_model_metrics.get('recall_macro', 0)
            f1_val_indo = indo_model_metrics.get('f1_macro', 0)
            
            c_row1_col1, c_row1_col2 = st.columns(2)
            c_row2_col1, c_row2_col2 = st.columns(2)
            
            c_row1_col1.metric("Accuracy", f"{acc_val_indo*100:.2f}%")
            c_row1_col2.metric("Precision", f"{prec_val_indo*100:.2f}%")
            c_row2_col1.metric("Recall", f"{rec_val_indo*100:.2f}%")
            c_row2_col2.metric("F1 Score", f"{f1_val_indo*100:.2f}%")
        else:
            st.error("Metrik IndoBERT tidak ditemukan!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Confusion Matrix
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("B. Confusion Matrix Model (SVM Baru vs IndoBERT)")
    st.markdown("Matriks kebingungan menunjukkan detail pemetaan distribusi prediksi model terhadap label aktual.")
    
    svm_cm = None
    if svm_model_metrics:
        svm_cm = np.array(svm_model_metrics.get('confusion_matrix', [[0,0,0],[0,0,0],[0,0,0]]))
    indo_cm = None
    indo_testset_metrics_path = "models/indobert_sentiment/metrics_indobert.json"
    if os.path.exists(indo_testset_metrics_path):
        with open(indo_testset_metrics_path, 'r', encoding='utf-8') as f:
            indo_testset_metrics = json.load(f)
            indo_cm = np.array(indo_testset_metrics.get('confusion_matrix', [[0,0,0],[0,0,0],[0,0,0]]))
            
    labels = ['negatif', 'netral', 'positif']
    label_ui = {'negatif': 'Negatif', 'netral': 'Netral', 'positif': 'Positif'}
    x = [label_ui.get(l, l) for l in labels]
    y = [label_ui.get(l, l) for l in labels]
    
    col_cm1, col_cm2 = st.columns(2)
    with col_cm1:
        st.markdown("<h4 style='color:#1a2744; text-align:center;'>Confusion Matrix SVM</h4>", unsafe_allow_html=True)
        if svm_cm is not None:
            fig_svm_cm = px.imshow(svm_cm, x=x, y=y, text_auto=True, color_continuous_scale='Blues')
            fig_svm_cm.update_layout(xaxis_title="Prediksi SVM", yaxis_title="Label Aktual")
            st.plotly_chart(apply_plotly_style(fig_svm_cm), use_container_width=True)
    with col_cm2:
        st.markdown("<h4 style='color:#1a2744; text-align:center;'>Confusion Matrix IndoBERT</h4>", unsafe_allow_html=True)
        if indo_cm is not None:
            fig_indo_cm = px.imshow(indo_cm, x=x, y=y, text_auto=True, color_continuous_scale='Greens')
            fig_indo_cm.update_layout(xaxis_title="Prediksi IndoBERT", yaxis_title="Label Aktual")
            st.plotly_chart(apply_plotly_style(fig_indo_cm), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Agreement Analysis
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("C. Analisis Keselarasan Label (Agreement Analysis)")
    
    agreement_rate = (df_display['sentiment_rating'] == df_display['sentiment_indobert']).mean() * 100
    mismatch_rate = 100 - agreement_rate
    
    col_ag1, col_ag2 = st.columns(2)
    with col_ag1:
        st.metric("Agreement Rate (Kesesuaian)", f"{agreement_rate:.2f}%")
    with col_ag2:
        st.metric("Mismatch Rate (Ketidaksesuaian)", f"{mismatch_rate:.2f}%")
        
    st.markdown("""
    <p style='color:#4a5568; font-size:13px; margin-top:15px;'>
    * <strong>Agreement Rate</strong> merepresentasikan persentase ulasan yang menunjukkan kesamaan polaritas antara rating bintang (skala numerik) dan prediksi berbasis teks oleh model.<br>
    * <strong>Mismatch Rate</strong> merepresentasikan persentase ulasan yang menunjukkan ketidaksesuaian polaritas, di mana rating bintang numerik tidak selaras dengan isi teks opini tertulis.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mismatch Analysis
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("D. Pemetaan Jenis Ketidaksesuaian (Mismatch Analysis)")
    
    mismatch_counts = get_mismatch_analysis(df_display)
    if len(mismatch_counts) > 0:
        fig_mismatch_bar = px.bar(
            x=mismatch_counts.values, y=mismatch_counts.index, orientation='h',
            color=mismatch_counts.index,
            color_discrete_map={
                'Positif Rating → Negatif Teks': '#EF4444', 
                'Negatif Rating → Positif Teks': '#10B981',
                'Netral Rating → Positif Teks': '#6366F1', 
                'Netral Rating → Negatif Teks': '#F59E0B'
            },
            labels={'x': 'Jumlah Sampel', 'y': 'Tipe Ketidaksesuaian'}
        )
        st.plotly_chart(apply_plotly_style(fig_mismatch_bar), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interpretasi Hasil
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("E. Interpretasi Hasil Analisis Evaluasi")
    
    indo_accuracy = indo_model_metrics['test_accuracy'] * 100 if indo_model_metrics else 0
    st.markdown(f"""
    * Model IndoBERT berhasil mencapai akurasi sebesar **{indo_accuracy:.2f}%** pada dataset pengujian, yang mengonfirmasi kapabilitas tinggi model berbasis arsitektur Transformer dalam mengolah teks ulasan informal.
    * Nilai Agreement Rate sebesar **{agreement_rate:.2f}%** menunjukkan bahwa sebagian besar label klasifikasi kontekstual teks ulasan selaras dengan rating bintang bawaan pengguna.
    * Temuan tingkat ketidaksesuaian (mismatch) sebesar **{mismatch_rate:.2f}%** mengindikasikan adanya fenomena bias rating, di mana pemberian rating numerik pengguna seringkali tidak mencerminkan polaritas teks opini tertulis yang sebenarnya.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "⚙️ Pipeline Praproses":
    st.title("Pipeline Pengolahan Data")
    
    # Flowchart Penelitian
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("1. Alur Penelitian")
    st.graphviz_chart('''
        digraph {
            rankdir=TB;
            fontname="Inter, Arial";
            fontsize=12;
            node [shape=box, style="filled,rounded", color="#CBD5E1", fillcolor="#FFFFFF", fontname="Inter, Arial", penwidth=1.5];
            edge [color="#6366F1", penwidth=2];
            
            A [label="1. Scraping Review\\n(Google Play Store)", fillcolor="#EEF2FF", color="#818CF8"];
            B [label="2. Cleaning Minimal\\n(hapus emoji, URL, tag HTML,\\nrapikan spasi berlebih)", fillcolor="#EEF2FF", color="#818CF8"];
            C1 [label="3a. Sampling Manual\\n(Cochran, n=382) + Label Manual", fillcolor="#EEF2FF", color="#818CF8"];
            C2 [label="3b. Auto-Labeling Teks Natural\\n(Teacher: RoBERTa)", fillcolor="#EEF2FF", color="#818CF8"];
            M [label="4. Merge Label Final\\n(RoBERTa + Manual)", fillcolor="#EEF2FF", color="#818CF8"];
            D [label="5a. Modeling SVM + TF-IDF\\n(praproses penuh di sini, Baseline)", fillcolor="#ECFDF5", color="#34D399"];
            E [label="5b. Fine-tuning IndoBERT\\n(teks natural, Model Utama)", fillcolor="#ECFDF5", color="#34D399"];
            F1 [label="6a. Evaluasi SVM\\n(Accuracy, Precision, Recall, F1,\\nAUC-ROC, Confusion Matrix)", fillcolor="#ECFDF5", color="#34D399"];
            F2 [label="6b. Evaluasi IndoBERT\\n(Accuracy, Precision, Recall, F1,\\nAUC-ROC, Confusion Matrix)", fillcolor="#ECFDF5", color="#34D399"];
            F3 [label="6c. Perbandingan Model\\n(Apple-to-Apple: split & label identik)", fillcolor="#ECFDF5", color="#34D399"];
            G [label="7. Analisis Tren Temporal\\n(model terpilih)", fillcolor="#FFFBEB", color="#FBBF24"];
            H [label="8. Dashboard Visualisasi\\n(Streamlit)", fillcolor="#FFFBEB", color="#FBBF24"];

            A -> B;
            B -> C1;
            B -> C2;
            C1 -> M;
            C2 -> M;
            M -> D;
            M -> E;
            D -> F1;
            E -> F2;
            F1 -> F3;
            F2 -> F3;
            F3 -> G -> H;
        }
    ''')
    st.markdown("""
**Penjelasan Tahap 2 — Cleaning Minimal.** Tahap ini hanya membersihkan derau (*noise*) non-linguistik yang tidak membawa muatan sentimen, tanpa mengubah struktur kalimat. Operasi yang dilakukan tepatnya ada empat: (1) menghapus emoji dan simbol piktografis; (2) menghapus URL/tautan; (3) menghapus tag HTML jika ada; serta (4) merapikan spasi berlebih menjadi spasi tunggal. Teks hasil tahap ini disebut *teks natural* karena huruf kapital, imbuhan, kata hubung, dan tanda baca tetap dipertahankan apa adanya.

**Mengapa tidak dipraproses penuh di sini?** Praproses penuh (*case folding*, *stemming*, *stopword removal*, penandaan negasi) justru menghapus informasi yang dibutuhkan model berbasis *Transformer*: RoBERTa dan IndoBERT memahami makna dari konteks urutan kata, sehingga imbuhan dan kata hubung yang dibuang oleh *stemming*/*stopword removal* akan merusak representasi kontekstualnya. Sebaliknya, SVM + TF-IDF bekerja atas frekuensi kata lepas (*bag-of-words*) sehingga tetap memerlukan praproses penuh — karena itu praproses penuh dipindah dan hanya dipanggil di Tahap 5a.

**Tahap 6 dipisah menjadi tiga.** Setiap model dievaluasi secara mandiri terlebih dahulu (6a untuk SVM, 6b untuk IndoBERT) dengan metrik yang sama, baru kemudian hasil keduanya dipertemukan pada tahap perbandingan (6c). Perbandingan bersifat *apple-to-apple* karena kedua model dilatih dan diuji pada pembagian data (*split*) yang identik dengan label target yang sama.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Statistik Dataset
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("2. Statistik Deskriptif Dataset")
    
    min_date_dataset = df_display['at'].min().date() if not df_display.empty else "-"
    max_date_dataset = df_display['at'].max().date() if not df_display.empty else "-"
    
    col_st1, col_st2, col_st3 = st.columns(3)
    with col_st1:
        st.metric("Total Review", f"{len(df_display):,}")
    with col_st2:
        st.metric("Periode Pengambilan", f"{min_date_dataset} - {max_date_dataset}")
    with col_st3:
        st.metric("Sumber Data", "Google Play Store")
        
    if 'score' in df_display.columns:
        st.markdown("\nDistribusi Rating Bintang:")
        rating_counts = df_display['score'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['Rating', 'Jumlah']
        fig_rating = px.bar(rating_counts, x='Rating', y='Jumlah', 
                           color='Rating', color_discrete_sequence=['#EF4444', '#F97316', '#F59E0B', '#84CC16', '#10B981'])
        st.plotly_chart(apply_plotly_style(fig_rating), use_container_width=True)
        st.table(rating_counts)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Contoh Data
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("3. Perbandingan Data Teks Sebelum dan Sesudah Praproses")
    st.caption("Praproses penuh (stemming, stopword removal, penandaan negasi) di bawah ini khusus dipakai untuk SVM (Tahap 5a). IndoBERT (model utama) tidak memakai hasil ini - IndoBERT dilatih dari teks natural (cleaning minimal saja: hapus emoji/URL, tanpa stemming) supaya representasi kontekstualnya tidak rusak.")

    if 'content' in df_display.columns and 'cleaned_content' in df_display.columns:
        real_samples = df_display[df_display['content'].notna() & df_display['cleaned_content'].notna()].sample(n=min(5, len(df_display)), random_state=42)
        sample_data = pd.DataFrame({
            "Sebelum Preprocessing": real_samples['content'].tolist(),
            "Sesudah Preprocessing": real_samples['cleaned_content'].tolist()
        }).reset_index(drop=True)
        st.table(sample_data)
    else:
        st.info("Kolom 'content' atau 'cleaned_content' tidak ditemukan di dataset!")
    st.markdown("</div>", unsafe_allow_html=True)