```markdown
# FlyScrapper

FlyScrapper is a Python-based tool that automates the process of gathering flight details from various airline websites. By leveraging the capabilities of `pyppeteer` for browser automation and `easyocr` for optical character recognition, FlyScrapper navigates through the booking sections of specified URLs, logs in using captcha recognition, and scrapes available flight information such as prices, routes, and timings.

## Features

- Asynchronous web scraping for efficiency
- Automated captcha solving for login processes
- Flexibility to specify flight search parameters
- Ability to scrape multiple websites concurrently

## Installation

To use FlyScrapper, you need to have Python installed on your machine. You can then set up the project's environment with the following steps:

```bash
# Clone the repository
git clone https://github.com/your-username/flyscrapper.git
cd flyscrapper

# It's recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt
```

## Usage

To start using FlyScrapper, modify the `urls` list in the script with the login URLs of the flight websites you wish to scrape. Also, you can customize the `fly_info` dictionary to set your desired flight search parameters.

Run the script:

```bash
python fly_scrapper.py
```

## Configuration

### Flight Search Parameters

By default, FlyScrapper is configured to search for one-way flights from Mashhad (MHD) to Tehran (THR) using the current date. You can modify the parameters by changing the `fly_info` dictionary within the script:

```python
inf = {
    'fromCity': 'MHD',
    'toCity': 'THR',
    'wayType': 'OneWay',
    'flyDate': '1402/10/11' # Date in jdatetime format (YYYY/MM/DD)
}
```

### OCR Language

The `Reader` from `easyocr` is set to recognize both English (`en`) and Farsi/Persian (`fa`). If you need other languages or only one of these, adjust the `Reader` initialization:

```python
reader = Reader(lang_list=['en', 'fa'], gpu=False) # Set to `gpu=True` if you want to use GPU acceleration
```

## Contributing

If you'd like to contribute to FlyScrapper, your help is very much appreciated. Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- Thanks to the `pyppeteer` and `easyocr` communities for the incredible resources.
- This project is not affiliated with any of the flight websites it accesses and is intended for educational purposes only.

## Disclaimer

This software is for educational purposes only. Using this script to scrape websites might be against the Terms of Service of the websites. Use it responsibly and ethically.
```

Be sure to update the URL to the repository where it says `https://github.com/your-username/flyscrapper.git` with the correct URL. Also, you might want to include more details, like a `CONTRIBUTING.md` document or add a `LICENSE` file if there isn't one already. Always check and ensure you're permitted to scrape the websites you intend to target and respect their bots.txt file and terms of service.