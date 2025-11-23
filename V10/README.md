# Tribology Experiment Data Analysis

This project provides a Python-based solution for processing experimental tribology data, performing error analysis, and generating plots as required for your presentation.

## Project Structure

tribology_analysis/
├── data/
│ ├── integrated_experiment_data.csv # Consolidated raw data after parsing
│ └── (other intermediate data files)
├── plots/
│ ├── mu_vs_normal_force.png
│ ├── mu_vs_normal_area.png
│ └── mu_vs_voltage.png
├── src/
│ ├── data_parser.py # Handles parsing raw data from image-like structures
│ ├── error_analysis.py # Contains functions for error propagation and statistical analysis
│ ├── plot_generator.py # Generates various plots with error bars
│ └── main.py # Main script to run the analysis workflow
├── requirements.txt # Python dependencies
└── README.md # Project README

## Setup and Installation

1.  **Clone the repository (or create the files manually):**
    ```bash
    git clone <repository_url>
    cd tribology_analysis
    ```
    (If you are creating files manually, ensure the directory structure above is followed).

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

1.  **Review and Update Data (Crucial Step):**
    The `src/data_parser.py` contains hardcoded data based on your images. **Crucially, the `main.py` file contains placeholder values for "Normal Force (Fn)" and its uncertainty (Delta_Fn) in the `mass_config_mapping` dictionary and for the voltage experiment data.**

    **Before running `main.py`, you MUST:**
    *   **Update `mass_config_mapping` in `main.py`:** Replace the placeholder mass values and their uncertainties with your precise experimental measurements for each `Block_Config`.
    *   **Update `Fn_avg` and `Fn_delta` for `Grosse_Flaeche_Spannung` in `main.py`:** Define how normal force is determined for the voltage experiments and provide the correct average and uncertainty.

2.  **Run the analysis:**
    Execute the `main.py` script from the project root directory:
    ```bash
    python src/main.py
    ```

## Output

*   **`data/integrated_experiment_data.csv`**: A CSV file containing all parsed and consolidated raw data. This is an intermediate file for review.
*   **`plots/` directory**: Contains the generated plots:
    *   `mu_vs_normal_force.png`: Friction coefficient (μ) vs. Normal Force (m*g).
    *   `mu_vs_normal_area.png`: Friction coefficient (μ) vs. Normal Area (A).
    *   `mu_vs_voltage.png`: Friction coefficient (μ) vs. Voltage (U).
*   Console output will display intermediate steps and error analysis examples.

## Error Analysis Approach

This project primarily uses **Method 2 (Systematischer Fehler)** as preferred in your instructions:
*   For measurements with an interval (`X-Y`), the average (`(X+Y)/2`) is used as the central value, and half of the range (`(Y-X)/2`) is used as the uncertainty (ΔF).
*   For friction coefficient (μ) and its uncertainty (Δμ), the general formula for error propagation is applied:
    $$ \Delta \mu = \sqrt{\left(\frac{1}{F_N} \Delta F_R\right)^2 + \left(\frac{F_R}{F_N^2} \Delta F_N\right)^2} $$
*   Standard deviation (σ68), Standard Error of the Mean (SEM), and Confidence Interval (c95) are **not calculated** for individual friction force measurements in Method 2, as the interval is treated as a systematic error due to apparatus limitations. The script will output "nicht betrachtet" for these values in the examples.

**Mention of Method 1 (Statistical Analysis):**
The `error_analysis.py` module includes a function `calculate_error_method_1` that demonstrates how Method 1 (treating interval boundaries as N=6 independent measurements for statistical analysis) could be implemented. This can be used for discussion in your presentation, as requested.

## Presentation Points (according to your PDF)

1.  **First page / slide:** D-MATL, Practicum I, Tribology, group No., names of group members, date (month and year)
2.  **Content overview**
3.  **(Short) Introduction**
4.  **Presentation of the experimental setup including pictures**
5.  **Measurement results in form of 3 plots with vertical error bars:**
    *   `friction coefficient μ versus normal force m g` (Generated as `plots/mu_vs_normal_force.png`)
    *   `friction coefficient μ versus normal area A` (Generated as `plots/mu_vs_normal_area.png`) - *Note: If contact area is constant for a given material in Tribologie data, this plot might not show much variation and serves as a point for discussion on experimental design.*
    *   `friction coefficient μ versus voltage U` (Generated as `plots/mu_vs_voltage.png`)
6.  **Error calculation:**
    *   Present the general formula for the error propagation Δy for a function y(x1,x2) with two variables x1 and x2 and their errors Δx1 and Δx2.
    *   Apply that to μ = F / (m g) with two variables F and m and present the resulting formula.
    *   Present the formula for the most common type of the standard deviation and the confidence interval, called σ68 and c95.
    *   Show three specific examples by presenting three filled templates by using the data of three selected data points. (Refer to the console output from `error_analysis_example()` in `main.py`).
7.  **(Short) discussion of the results**
8.  **Appendix:**
    *   Original measurement data, e.g. in form of a picture / pictures of them
    *   Lines of a created program for data evaluation (e.g. Python) - *You can include the Python scripts from `src/` here.*

## Important Notes

*   **Mass and Normal Force:** Ensure you replace the placeholder mass values (`mass_config_mapping`) in `main.py` with your accurate experimental masses (in grams). The script converts them to kilograms for normal force calculation.
*   **Kontaktflaeche:** The `Kontaktflaeche_cm2` is mapped based on your specified values. Verify these are correct for all relevant data points.
*   **Voltage Experiment Fn:** For the `mu_vs_voltage.png` plot, a placeholder `Fn_avg` and `Fn_delta` are used. You must determine the correct normal force and its uncertainty for your voltage experiments and update `main.py` accordingly.
*   **Method 1 vs Method 2:** The project prioritizes Method 2 for actual calculations and plots. Remember to discuss both approaches in your presentation. Method 1 (statistical calculation of std dev, SEM, c95) is demonstrated as a function `calculate_error_method_1` in `error_analysis.py` for illustrative purposes.