# MineSpider AI Web Dashboard

A local Flask website for your trained MineSpider Person + Rockfall YOLO models.

## Expected model locations

C:\MineSpider\models\person_model.pt
C:\MineSpider\models\rock_model.pt

## Setup

Open PowerShell:

    cd C:\MineSpider\minespider_web

    python -m venv venv
    .\venv\Scripts\activate

    pip install -r requirements.txt

Then:

    python app.py

Open:

    http://127.0.0.1:5000

Upload a JPG/PNG/WEBP mine image and click RUN AI DETECTION.

Person boxes are blue.
Rockfall boxes are red.

This is a prototype/operator-assisted demonstration and not a certified mine-safety system.
