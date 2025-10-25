# 📊 WhatsApp Chat Analyzer

A powerful and interactive web app built using **Python** and **Streamlit** that helps you analyze your WhatsApp chat data — from total messages and emoji usage to daily activity, most active users, and word clouds.

---

## 🚀 Features

- 📈 **Top Statistics** — total messages, words, media, and links  
- 👥 **Most Active Users** — see who chats the most  
- 🕒 **Timeline Analysis** — daily, monthly, and yearly chat trends  
- 💬 **Word Cloud** — visualize your most used words  
- 😂 **Emoji Analysis** — find your most used emojis  
- 📅 **Busy Day & Hour** — discover when your group is most active  
- 🔍 **Filter by User** — analyze chats of specific people  
- ⚙️ **Automatic Data Cleaning** — removes system messages and users with fewer than 5 messages
- 📈 **Automatic PDF Report generation** - Generates PDF report with all graphs 

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend / UI** | [Streamlit](https://streamlit.io) |
| **Data Analysis** | [Pandas](https://pandas.pydata.org) |
| **Visualization** | [Matplotlib](https://matplotlib.org), [Seaborn](https://seaborn.pydata.org), [WordCloud](https://amueller.github.io/word_cloud/) |
| **Language** | Python 3.x |

---

## 📁 Project Structure

```
Whatsapp-analyzer/
│
├── app.py                 # Main Streamlit application
├── helper.py              # Functions for analysis
├── preprocessor.py        # Chat data cleaning and preprocessing
├── requirements.txt       # Required dependencies
├── README.md              # Project documentation
└── myenv/                 # Virtual environment (excluded in .gitignore)
```

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Garvithindoliya16/Whatsapp_chat_analyzer.git
cd Whatsapp_chat_analyzer
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv myenv
myenv\Scripts\activate     # on Windows
# source myenv/bin/activate  # on macOS/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app
```bash
streamlit run app.py
```

### 5️⃣ Upload your WhatsApp chat file  
Go to **WhatsApp → Export Chat → Without Media**, and upload the `.txt` file in the app.

---

## 💡 Future Enhancements

- Add sentiment analysis  
- Compare chats between users  
- Support for multiple chat file formats 

---

## 🧑‍💻 Author

**Garvit Hindoliya**  
📧 garvithindoliya16@zohomail.in  
🌐 [GitHub Profile](https://github.com/Garvithindoliya16)

---

## 🪪 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
