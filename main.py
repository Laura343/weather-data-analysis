from scraper import run_scraper
from daily_processor import run_daily_processor
from daily_plotter import run_daily_plotter
from weekly_processor import run_weekly_processor
from weekly_plotter import run_weekly_plotter

def main():
    run_scraper()
    run_daily_processor()
    run_weekly_processor()
    run_daily_plotter()
    run_weekly_plotter()

if __name__ == "__main__":
    main()
