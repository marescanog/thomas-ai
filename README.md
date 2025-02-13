
# Thomas A.I.

Trackable Helper for Organized inventory Management and Autonomous Scanning A.I. This is the capstone project for the Seneca 2025 Artificial Intelligence Program.




## How to Run Locally

1 - Clone the project

```bash
  git clone https://github.com/marescanog/thomas-ai.git
```

2 - Go to the project directory

```bash
  cd my-project
```

Optional: Create virtual environment 

```bash
  python3 -m venv django_capstone_thomas
```

Optional: Use the virtual environment on your workspace

```bash
  # For VS Code
  # Ctrl + Shift + p
  # Python: Select Interpreter
  # Select django_capstone_thomas
  # You'll know if you selected the environment on bottom right
```

Alternatively, you can just skip the virtual environment creation
and just directly 

3 - Install dependencies

```bash
  pip install Django Pillow ultralytics numpy 
```

4 - Get a copy of the local db from Marvie & save it in the root

5 - Get a copy of .env from Marvie & save it in the root

6 - Start the server

```bash
export $(grep -v '^#' .env | xargs)
python manage.py runserver
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`APP_HOST`

## API Reference

#### Classify an image

```http
  POST /classification/classify/
```

Returns
- detected: detection list of class labels (array of strings)
- highest_score: object
    - The object with highest confidence score
    - contains: product_id, product_name, class_label_name, product_type, alcohol_volume, category
- raw_detections: all objects detected (array of objects)
    - contains: class_index, confidence, box




## Documentation

[Documentation](https://tropical-mail-658.notion.site/Thomas-ai-Documentation-199081aada9b804c846fe7de0bede35b?pvs=4)

