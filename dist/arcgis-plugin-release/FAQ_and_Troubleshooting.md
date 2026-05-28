# Idox Geospatial — GSQIS Toolbox for ArcGIS Pro
## Frequently Asked Questions & Troubleshooting Guide

**Version:** 1.0  
**Compatible with:** ArcGIS Pro 3.0 and above  
**Support:** [geo-customersupport@idoxgroup.com](mailto:geo-customersupport@idoxgroup.com)  
**SDK & Resources:** [https://sdk.idoxgeospatial.co.uk/](https://sdk.idoxgeospatial.co.uk/)

---

## Frequently Asked Questions (FAQ)

---

### General Questions

**Q: What is the GSQIS Toolbox?**  
The GSQIS Toolbox is an ArcGIS Pro plugin (Python Toolbox) developed by Idox Geospatial. It provides geospatial analysis tools — starting with the **Layer Statistics** tool, which summarises the data in any feature layer and exports a readable report.

---

**Q: Which versions of ArcGIS Pro does the toolbox support?**  
The GSQIS Toolbox is supported on **ArcGIS Pro 3.0 and above** running on Windows 10 or Windows 11 (64-bit).

---

**Q: Do I need administrator rights to install the toolbox?**  
No administrator rights are required, as long as you extract the toolbox files to a folder you have full access to (e.g., your Documents folder or a dedicated GIS tools folder). Avoid placing files in `C:\Program Files\` or other system-protected directories.

---

**Q: Does the toolbox require an internet connection?**  
No. The toolbox works entirely offline after installation.

---

**Q: Do I need to install any additional software or Python packages?**  
No. The toolbox uses only **`arcpy`**, which is built into ArcGIS Pro. No additional Python libraries need to be installed.

---

**Q: Can I use the toolbox with ArcGIS Desktop (ArcMap) instead of ArcGIS Pro?**  
No. The GSQIS Toolbox is designed specifically for **ArcGIS Pro 3.0+** and is not compatible with ArcGIS Desktop (ArcMap).

---

**Q: Will the toolbox affect my existing projects or data?**  
No. The toolbox only reads your data to compute statistics — it never modifies your source layers. The only output it creates is the text report file you specify.

---

**Q: Can I add the toolbox to multiple ArcGIS Pro projects?**  
Yes. You can add the same `GSQIS_Toolbox.pyt` file to as many ArcGIS Pro projects as you like. Simply follow the installation steps (right-click **Toolboxes → Add Toolbox**) in each project.

---

**Q: What types of data does the Layer Statistics tool support?**  
The Layer Statistics tool works with any **vector feature layer** (points, lines, or polygons). This includes shapefiles, file geodatabase feature classes, enterprise geodatabase layers, and in-memory layers.

---

**Q: What does the output report contain?**  
The output is a plain-text (`.txt`) file with two sections:
1. **LAYER SUMMARY** — basic layer information (name, coordinate system, geometry type, feature count, field count).
2. **FIELD STATISTICS** — per-field statistics:
   - *Numeric fields*: count, minimum, maximum, mean, median, sum, standard deviation.
   - *Text/categorical fields*: count, empty value count, number of unique values, and the most frequently occurring values.

---

## Troubleshooting

---

### Problem: The toolbox does not appear in the Catalog pane after adding it

**Possible causes and solutions:**

1. **The wrong file type was selected.** Make sure you selected the file `GSQIS_Toolbox.pyt` (not a folder or a different file). The `.pyt` extension indicates an ArcGIS Pro Python Toolbox.

2. **The Catalog pane needs refreshing.** Right-click **Toolboxes** in the Catalog pane and select **Refresh**.

3. **The toolbox was not added to the correct project.** Check that the project currently open in ArcGIS Pro is the one you intended to add the toolbox to.

---

### Problem: The Layer Statistics tool fails with an error message

**Error: "ERROR 000732: Input Features: Dataset does not exist or is not supported"**

- The selected layer is not a valid vector feature layer. Ensure you have loaded a vector layer (shapefile or feature class) into your map before running the tool.

---

**Error: "ERROR 000210: Cannot create output …"**

- The output report file path you specified is not writable.
- Try saving the output to a folder you own, such as `C:\Users\YourName\Documents\`.
- Avoid paths on read-only network drives.

---

**Error: "ExecuteError: Failed to execute (LayerStatistics)"**

- Try restarting ArcGIS Pro and re-running the tool.
- Ensure the input layer is fully loaded (visible on the map with features).
- If the error persists, please contact support (details below) and include the full error message from the **Messages** panel.

---

### Problem: The output report file is empty or shows no field statistics

- The input layer may contain no features. Open the layer's attribute table and check whether any rows are present.
- If the layer has features but no fields (other than the geometry field), the report will only show layer-level information.

---

### Problem: "Maximum Unique Values to Report" shows unexpected results

- This parameter controls how many unique text values are listed per field. The default is **20**. If you have fields with many unique values (e.g., unique identifiers), only the most frequently occurring 20 will be shown unless you increase this number.

---

### Problem: ArcGIS Pro is slow to open the tool or run the analysis

- Performance depends on the size of your dataset. Layers with millions of features may take several minutes to process.
- Consider testing first with a smaller subset of your data (right-click the layer → **Data → Export Features** to create a sample).

---

### Problem: The toolbox disappears after closing and reopening ArcGIS Pro

- Toolboxes added manually via **Add Toolbox** are saved to the **current project** (`.aprx` file). If you opened a different project, you will need to re-add the toolbox.
- To avoid this, save your project after adding the toolbox (**Ctrl + S**).

---

### Problem: I see a yellow warning triangle next to the toolbox

- This usually means the `.pyt` file has been moved or deleted from its original location.
- Re-add the toolbox by right-clicking **Toolboxes → Add Toolbox** and browsing to the correct location of `GSQIS_Toolbox.pyt`.

---

## Still Need Help?

If your issue is not listed above or you are unable to resolve it, please contact the Idox Geospatial support team:

| Channel | Details |
|---------|---------|
| **Email support** | [geo-customersupport@idoxgroup.com](mailto:geo-customersupport@idoxgroup.com) |
| **SDK & documentation** | [https://sdk.idoxgeospatial.co.uk/](https://sdk.idoxgeospatial.co.uk/) |

**When emailing support, please include:**
- Your full name and organisation
- Your ArcGIS Pro version (e.g., *3.2.0*)
- Windows version (e.g., *Windows 11 64-bit*)
- A description of the problem
- Any error messages shown in ArcGIS Pro (copy/paste the text from the **Messages** panel)

We aim to respond within one business day.

---

*© Idox Geospatial. All rights reserved.*  
*GSQIS Toolbox for ArcGIS Pro — v1.0*
