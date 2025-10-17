# Pose Image Collector

**Pose Image Collector** is a Python-based tool that fetches and organizes publicly available photo URLs from the [Pexels API](https://www.pexels.com/api/).  
It automatically categorizes photos into different pose types (e.g., standing, sitting, hands on hips, etc.) and stores metadata in an SQLite database for easy integration with apps that suggest poses based on context or location.

---

## 🚀 Features
- Uses the Pexels API to safely collect photo URLs.
- Categorizes images by pose type (e.g., standing, sitting, side pose, etc.).
- Stores image metadata (URL, photographer, category) in a local SQLite database.
- Prevents frequent API hits to avoid rate limits.
- Ready for integration with recommendation or pose-suggestion apps.

---

## 🧰 Requirements
- Python 3.8+
- Pexels API Key (free to get from [Pexels Developers](https://www.pexels.com/api/))

Install dependencies:
```bash
pip install requests
