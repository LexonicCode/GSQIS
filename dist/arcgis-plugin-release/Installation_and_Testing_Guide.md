# Idox Geospatial — GSQIS Toolbox for ArcGIS Pro
## Installation & Testing Guide

**Version:** 1.0  
**Compatible with:** ArcGIS Pro 3.0 and above  
**Support:** [geo-customersupport@idoxgroup.com](mailto:geo-customersupport@idoxgroup.com)  
**SDK & Resources:** [https://sdk.idoxgeospatial.co.uk/](https://sdk.idoxgeospatial.co.uk/)

---

> **Welcome!** This guide walks you through installing and testing the GSQIS Toolbox inside ArcGIS Pro. No technical background is required — just follow each step in order.

---

## Contents

1. [Before You Start — Prerequisites](#1-before-you-start--prerequisites)
2. [What's in the Package](#2-whats-in-the-package)
3. [Installation](#3-installation)
4. [Running Your First Analysis](#4-running-your-first-analysis)
5. [Verifying Successful Installation](#5-verifying-successful-installation)
6. [Uninstalling the Toolbox](#6-uninstalling-the-toolbox)
7. [Getting Help](#7-getting-help)

---

## 1. Before You Start — Prerequisites

Before installing the GSQIS Toolbox, please confirm the following:

| Requirement | Details |
|-------------|---------|
| **ArcGIS Pro** | Version 3.0 or later (see [How to check your version](#check-version)) |
| **Operating System** | Windows 10 or Windows 11 (64-bit) |
| **User Permissions** | You must be able to add files and toolboxes within ArcGIS Pro |
| **Disk Space** | At least 5 MB free |

> **Note:** No internet connection or additional software installation is required to use the toolbox.

### Check Your ArcGIS Pro Version {#check-version}

1. Open **ArcGIS Pro**.
2. Click the **Project** tab in the top-left ribbon.
3. Select **About ArcGIS Pro** at the bottom of the left panel.
4. Your version number is shown at the top of that page (e.g., *ArcGIS Pro 3.2.0*).

If your version is below 3.0, please contact your GIS administrator or Esri support to upgrade before proceeding.

---

## 2. What's in the Package

The distribution ZIP file (`GSQIS-ArcGIS-Toolbox-v1.0.zip`) contains:

```
GSQIS-ArcGIS-Toolbox-v1.0/
├── GSQIS_Toolbox.pyt                       ← The ArcGIS Pro toolbox file
├── Installation_and_Testing_Guide.md       ← This guide (Markdown)
├── Installation_and_Testing_Guide.pdf      ← This guide (PDF)
├── FAQ_and_Troubleshooting.md              ← Frequently asked questions
└── FAQ_and_Troubleshooting.pdf             ← Frequently asked questions (PDF)
```

The file you need to install is **`GSQIS_Toolbox.pyt`**.

---

## 3. Installation

### Step 1 — Unzip the Package

1. Right-click **`GSQIS-ArcGIS-Toolbox-v1.0.zip`** in Windows File Explorer.
2. Select **Extract All…**
3. Choose a convenient folder (for example, `C:\GIS\Tools\GSQIS\`) and click **Extract**.
4. Make a note of the folder path — you will need it in Step 3.

> **Tip:** Avoid extracting to a network drive or a folder that requires administrator access (e.g., `C:\Program Files\`). Your Documents folder or a dedicated GIS tools folder works best.

---

### Step 2 — Open ArcGIS Pro

Open ArcGIS Pro and either open an existing project or create a new one.

> **New to ArcGIS Pro projects?** From the splash screen, choose **Map** under *New Project* to create a blank project.

---

### Step 3 — Add the Toolbox to Your Project

1. In the **Catalog** pane on the right side of the screen, look for the **Toolboxes** section.
   - If the Catalog pane is not visible, click **View** in the top ribbon, then select **Catalog Pane**.

2. Right-click **Toolboxes** and choose **Add Toolbox**.

   ![Add Toolbox menu](https://sdk.idoxgeospatial.co.uk/)

3. In the file browser that opens, navigate to the folder where you extracted the ZIP file (Step 1).

4. Select **`GSQIS_Toolbox.pyt`** and click **OK**.

5. The toolbox will now appear under **Toolboxes** in the Catalog pane, labelled **GSQIS Toolbox**.

---

### Step 4 — Confirm the Toolbox is Listed

After adding the toolbox, you should see:

```
Toolboxes
└── GSQIS Toolbox
    └── Analysis
        └── Layer Statistics
```

If you can see **Layer Statistics** listed under **Analysis**, the installation is complete.

---

## 4. Running Your First Analysis

The **Layer Statistics** tool computes a summary of all data fields in any feature layer — giving you counts, minimum/maximum values, averages, and more — and saves the results to a text file.

### Steps

1. **Load a layer** into your ArcGIS Pro map (if you don't already have one):
   - In the **Catalog** pane, browse to any shapefile or feature class.
   - Right-click it and choose **Add To Current Map**.

2. **Open the Layer Statistics tool:**
   - In the Catalog pane, expand **Toolboxes → GSQIS Toolbox → Analysis**.
   - Double-click **Layer Statistics**.
   - The tool dialog opens in the **Geoprocessing** pane.

3. **Configure the tool parameters:**

   | Parameter | What to enter |
   |-----------|--------------|
   | **Input Feature Layer** | Select your loaded layer from the dropdown |
   | **Output Report File** | Click the folder icon and choose where to save the report (e.g., `C:\GIS\Output\my_layer_stats.txt`) |
   | **Maximum Unique Values to Report** | Leave as `20` (the default) unless you want more or fewer values listed for text fields |

4. Click **Run** (the blue button at the bottom of the Geoprocessing pane).

5. Watch the **Messages** section for progress. When you see:
   ```
   Report written to: C:\GIS\Output\my_layer_stats.txt
   ```
   the tool has finished successfully.

6. Open the output `.txt` file in Notepad or any text editor to review your layer statistics report.

---

## 5. Verifying Successful Installation

To confirm everything is working correctly:

- [ ] **GSQIS Toolbox** appears under **Toolboxes** in the Catalog pane.
- [ ] **Layer Statistics** tool opens when double-clicked.
- [ ] The tool runs without errors on a test layer.
- [ ] An output `.txt` report file is created at the path you specified.
- [ ] The report contains a **LAYER SUMMARY** section and a **FIELD STATISTICS** section.

If all five items above are ✅, your installation is successful.

---

## 6. Uninstalling the Toolbox

To remove the GSQIS Toolbox from your project:

1. In the **Catalog** pane, right-click **GSQIS Toolbox** under **Toolboxes**.
2. Select **Remove**.

This removes the toolbox from the current project only. To fully remove it from your computer, simply delete the extracted folder where `GSQIS_Toolbox.pyt` is stored.

> **Note:** Removing the toolbox does not delete any output reports you have already generated.

---

## 7. Getting Help

If you have questions or encounter any issues:

| Channel | Details |
|---------|---------|
| **Email support** | [geo-customersupport@idoxgroup.com](mailto:geo-customersupport@idoxgroup.com) |
| **SDK & documentation** | [https://sdk.idoxgeospatial.co.uk/](https://sdk.idoxgeospatial.co.uk/) |

When contacting support, please include:
- Your ArcGIS Pro version number
- A description of the issue or error message
- The name of the layer you were working with (if applicable)

---

*© Idox Geospatial. All rights reserved.*  
*GSQIS Toolbox for ArcGIS Pro — v1.0*
