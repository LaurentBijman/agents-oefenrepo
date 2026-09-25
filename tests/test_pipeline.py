from sales_forecast.pipeline import main, run


def test_run_weekly_forecast(write_csv):
    path = write_csv(
        "2024-01-01,koffie,10,3.50\n"
        "2024-01-08,koffie,10,3.50\n"
        "2024-01-15,koffie,10,3.50\n"
        "2024-01-15,thee,99,2.00\n"
    )

    result = run(path, period="week", horizon=2, products=["koffie"])

    assert result.method == "moving_average"
    assert result.values == [10.0, 10.0]


def test_main_prints_forecast(write_csv, capsys):
    path = write_csv("2024-01-01,koffie,1,1\n2024-01-02,koffie,3,1\n2024-01-03,koffie,5,1\n")

    exit_code = main([str(path), "--period", "day", "--horizon", "1", "--method", "linear_trend"])

    assert exit_code == 0
    assert "+1 day: 7.0" in capsys.readouterr().out
