#  Transistor Sizing Optimization using ABC Algorithm

##  Project Overview
This project implements an **Artificial Bee Colony (ABC) algorithm** to optimize transistor sizing for digital circuits.  
The optimization metric is the **Power-Delay Product (PDP)**, which is minimized by tuning transistor parameters in an LTspice netlist.

The project is based on a research paper that applied **metaheuristic optimization** to transistor sizing.  
We re-implemented the idea and connected it with **LTspice simulations** for realistic power and delay estimation.

---

##  Features
- Automatically modifies transistor size parameters in an LTspice netlist.
- Runs LTspice in batch mode to simulate circuits.
- Extracts **power** and **delay** from LTspice log files.
- Computes **Power-Delay Product (PDP)**.
- Uses **ABC optimization** to search for optimal transistor sizes.
- Reports the best transistor parameters and minimized PDP.

---

##  Project Structure
  
- **main.py** – Main Python script with ABC algorithm and LTspice integration  
- **delay_pr.net** – LTspice netlist file (circuit description with .param definitions)  
- **README.md** – Project documentation
- **DCMOS_PROJ_20T_delay_pr.asc** – LTspice schematic file  


##  Requirements
- **Python 3.8+**
- Python libraries:
  - `numpy`
  - `subprocess` (built-in)
  - `re` (built-in)
  - `os` (built-in)
- **LTspice** installed (tested with LTspice XVII).  
  - Update the `ltspice_path` in `main.py` with the path to your LTspice executable. Example:
    ```python
    ltspice_path = r"C:\Users\<username>\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
    ```

---

##  How to Run
1. Clone/download the project.
2. Place your LTspice netlist file (`.net`) in the project folder.  
   - Ensure the netlist contains a `.param N1` line where transistor parameters are defined.
3. Update paths in `main.py` if needed:
   - `netlist_path`
   - `log_path`
   - `ltspice_path`
4. Run the script:
   ```bash
   python main.py

