# LOINC Part Search

This project builds LOINC codes into a hierarchy based on LOINC part codes.  Hierarchies are base on the multi-axial hierarchy table. This is a demonstration project.  Features will gradually be expanded.  Searching capabilities will be added using part code terms and the LOINC code definitions. Data is from LOINC 2.65. The database contains all data from the loinc.txt and multi-axial hierarchy table.<br>
The project is designed as a set of layers,
* database containing loinc data stored in a object–attribute–value model design,
  * MySQL and Postgres databases are supported,
* connection layer that connects to the database and queries that database,
* parsing layer that converts query data into objects.
* object layer that is used to contain parsed data.<br>
A small set of rest-api using Flask are available.<br>
Part of LOINC 2.65 has been configured as a demonstration project.  The database contains only the codes below Human Leukocyte Antigen, LOINC part code: LP56928-2.  This is to stay within the Heroku 10,000 Postgres row limit for a demonstration project.<br><br>
See https://loinc.org/license/ for Regenstrief license for the use and distribution of LOINC.


# Documentation
1. [eav_object_design](./doc/eav_object_design.md): covers the design of the of data object containing loinc code data.
2. [db_design](./doc/db_design.md): database table layout.
3. [access_loinc_design](./doc/access_loinc_design.md):
4. [db_connection_design](./doc/db_connection_design.md):


# API Usage
## API Base URL: https://loinc-part-search-demo.herokuapp.com/

## Endpoints Summary
* GET: /loinc/&lt;code&gt;
  * GET: /loinc/parents/&lt;code&gt;
  * GET: /loinc/siblings/&lt;code&gt;
  * GET: /loinc/cousins/&lt;code&gt;
  * GET: /loinc/parts/&lt;code&gt;
    * GET: /loinc/parts/descendants/&lt;code&gt;
    * GET: /loinc/parts/parents/&lt;code&gt;

  
## Examples

### GET: /loinc/&lt;code&gt; 
Returns a json object with the description of this code.  Attributes are as described in the loinc.txt table.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/72323-9<br>
Example result:
```json
{
    defining definition: "LOINC code",
    LOINC code: "72323-9",
    preferred attribute: "Name",
    Name: "HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)",
    Short name: "HLA-DP+DQ+DR IgG Ser Ql FC",
    Common rank: "0",
    Class type: "1",
    Status: "ACTIVE",
    Class: "HLA",
    Method type: "Flow cytometry",
    Scale type: "Ord",
    System: "Ser",
    Time aspect: "Pt",
    Property: "PrThr",
    Component: "HLA-DP+DQ+DR Ab.IgG",
    parents: [
    "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
    ],
    children: [ ]
}
```


### GET: loinc/parents/&lt;code&gt;
Returns a json list of the parents of the LOINC code. The list contains one json for each parent.  Attributes are as described in the multi-axial table.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parents/72323-9<br>
Example result:<br>
```json
[
    {
        defining definition: "LOINC part code",
        LOINC part code: "LP97384-9",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR | Bld-Ser-Plas",
        parents: [
        "LOINC part code: LP56928-2, HLA-DP+DQ+DR"
        ],
        children: [
        "LOINC code: 72321-3, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Immunoassay",
        "LOINC code: 46995-7, HLA-DP+DQ+DR (class II) Ab in Serum",
        "LOINC code: 72323-9, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)"
        ]
    }
]
```


### GET: loinc/siblings/&lt;code&gt;
Returns a json list of the siblings of the LOINC code. Siblings are defined as all the children of the parents of the LOINC code. The list contains one json for each sibling, including the search code. In some sections of LOINC a part code can have both LOINC codes and LOINC part code as a child.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/siblings/72323-9<br>
Example result:<br>
```json
[
    {
        defining definition: "LOINC code",
        LOINC code: "72323-9",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)",
        Short name: "HLA-DP+DQ+DR IgG Ser Ql FC",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "Flow cytometry",
        Scale type: "Ord",
        System: "Ser",
        Time aspect: "Pt",
        Property: "PrThr",
        Component: "HLA-DP+DQ+DR Ab.IgG",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    },
    {
        defining definition: "LOINC code",
        LOINC code: "72321-3",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Immunoassay",
        Short name: "HLA-DP+DQ+DR IgG Ser Ql IA",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "IA",
        Scale type: "Ord",
        System: "Ser",
        Time aspect: "Pt",
        Property: "PrThr",
        Component: "HLA-DP+DQ+DR Ab.IgG",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    },
    {
        defining definition: "LOINC code",
        LOINC code: "46995-7",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) Ab in Serum",
        Short name: "HLA-DP+DQ+DR Ab NFr Ser",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "",
        Scale type: "Qn",
        System: "Ser",
        Time aspect: "Pt",
        Property: "NFr",
        Component: "HLA-DP+DQ+DR Ab",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    }
]
```




### GET: loinc/cousins/&lt;code&gt;
Returns a json list of the cousins of the LOINC code. Cousins are defined as all the children of the grand-parents of the LOINC code. The list contains one json for each cousin, including siblings and the search code. In some sections of LOINC a part code can have both LOINC codes and LOINC part code as a child.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/cousins/72323-9<br>
Example result:<br>
```json
[
    {
        defining definition: "LOINC code",
        LOINC code: "50019-9",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) [Type]",
        Short name: "HLA-DP+DQ+DR",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "",
        Scale type: "Nom",
        System: "Bld/Tiss",
        Time aspect: "Pt",
        Property: "Type",
        Component: "HLA-DP+DQ+DR",
        parents: [
        "LOINC part code: LP187542-8, HLA-DP+DQ+DR | Blood or Tissue"
        ],
        children: [ ]
    },
    {
        defining definition: "LOINC code",
        LOINC code: "72323-9",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)",
        Short name: "HLA-DP+DQ+DR IgG Ser Ql FC",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "Flow cytometry",
        Scale type: "Ord",
        System: "Ser",
        Time aspect: "Pt",
        Property: "PrThr",
        Component: "HLA-DP+DQ+DR Ab.IgG",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    },
    {
        defining definition: "LOINC code",
        LOINC code: "72321-3",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Immunoassay",
        Short name: "HLA-DP+DQ+DR IgG Ser Ql IA",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "IA",
        Scale type: "Ord",
        System: "Ser",
        Time aspect: "Pt",
        Property: "PrThr",
        Component: "HLA-DP+DQ+DR Ab.IgG",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    },
    {
        defining definition: "LOINC code",
        LOINC code: "46995-7",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR (class II) Ab in Serum",
        Short name: "HLA-DP+DQ+DR Ab NFr Ser",
        Common rank: "0",
        Class type: "1",
        Status: "ACTIVE",
        Class: "HLA",
        Method type: "",
        Scale type: "Qn",
        System: "Ser",
        Time aspect: "Pt",
        Property: "NFr",
        Component: "HLA-DP+DQ+DR Ab",
        parents: [
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ],
        children: [ ]
    }
]
```



### GET: loinc/parts/&lt;code&gt;
Returns a json object with the description of this part code.  Attributes are as described in the multi-axial table.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/LP97384-9<br>
Example result:<br>
```json
{
    defining definition: "LOINC part code",
    LOINC part code: "LP97384-9",
    preferred attribute: "Name",
    Name: "HLA-DP+DQ+DR | Bld-Ser-Plas",
    parents: [
      "LOINC part code: LP56928-2, HLA-DP+DQ+DR"
    ],
    children: [
        "LOINC code: 72321-3, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Immunoassay",
        "LOINC code: 46995-7, HLA-DP+DQ+DR (class II) Ab in Serum",
        "LOINC code: 72323-9, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)"
        ]
}
```



### GET: loinc/parts/parents/&lt;code&gt;
Returns a json list of the parents of the LOINC part code. The list contains one json for each parent.  Attributes are as described in the multi-axial table.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/parents/LP97384-9<br>
Example result:<br>
```json
[
    {
        defining definition: "LOINC part code",
        LOINC part code: "LP56928-2",
        preferred attribute: "Name",
        Name: "HLA-DP+DQ+DR",
        parents: [
        "LOINC part code: LP32739-2, Human Leukocyte Antigens"
        ],
        children: [
        "LOINC part code: LP187542-8, HLA-DP+DQ+DR | Blood or Tissue",
        "LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas"
        ]
    }
]
```



### GET: loinc/parts/descendants/&lt;code&gt;
Returns a json object listing the hierarchy below the search code.  The search code is the key to list of its children.  Each child is listed with a list of its children recursively.  Codes a listed with &lt;code type&gt;: code, name, e.g. LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas.<br>
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/descendants/LP56928-2<br>
Example result:<br>
```json
{
    LOINC part code: LP56928-2, HLA-DP+DQ+DR: [
        {
            LOINC part code: LP187542-8, HLA-DP+DQ+DR | Blood or Tissue: [
                  "LOINC code: 50019-9, HLA-DP+DQ+DR (class II) [Type]"
            ]
        },
        {
            LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas: [
                "LOINC code: 72321-3, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Immunoassay",
                "LOINC code: 46995-7, HLA-DP+DQ+DR (class II) Ab in Serum",
                "LOINC code: 72323-9, HLA-DP+DQ+DR (class II) IgG Ab [Presence] in Serum by Flow cytometry (FC)"
            ]
        }
    ]
}
```

