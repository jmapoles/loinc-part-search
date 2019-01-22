# LOINC Part Search

This is a project to build LOINC hierarchies based on LOINC part codes with searching capabilities.  Hierarchies are base on the multi-axial hierarchy table. Hierarchy support multiple parents for codes. This is a demonstration project. Search not support in this version.
Data is from LOINC 2.65.  The demonstration database contains only the codes below Human Leukocyte Antigen, LOINC part code: LP56928-2.  This is to stay within the Heroku 10,000 Postgres row limit for demonstration projects.
The project is configured as rest-API and returns json objects.


# API Usage
### API Base URL: https://loinc-part-search-demo.herokuapp.com/

## Endpoints Summary
* [`/loinc/<code>`](#loinc-code)
  * [`/loinc/parents/<code>`](#loinc-parents-code)
  * [`/loinc/siblings/<code>`](#loinc-sibling-<code>)
  * [`/loinc/cousins/<code>`](#loinc-cousins-<code>)
  * [`/loinc/parts/<code>`](#loinc-parts-<code>)
    * [`/loinc/parts/descendants/<code>`](#loinc-parts-descendants-<code>)
    * [`/loinc/parts/parents/<code>`](#loinc-parts-parents-<code>)
  
  
## Examples

### <a name="loinc-code"></a> loinc-code
Returns a json object with the description of this code.  Attributes are as described in the loinc.txt table.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/72323-9
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


### loinc/parents/<code>
Returns a json list of the parents of the LOINC code. The list contain one json for each parent.  Attributes are as described in the multi-axial table.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parents/72323-9
Example result:
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


### GET: loinc/siblings/<code>
Returns a json list of the siblings of the LOINC code. Siblings are defined as all the children of the parents of the LOINC code. The list contain one json for each sibling, including the search code. In some sections of LOINC a part code can have both LOINC codes and LOINC part code as a child.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/siblings/72323-9
Example result:
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




### GET: loinc/cousins/<code>
Returns a json list of the cousins of the LOINC code. Cousins are defined as all the children of the grand-parents of the LOINC code. The list contain one json for each cousin, including siblings and the search code. In some sections of LOINC a part code can have both LOINC codes and LOINC part code as a child.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/cousins/72323-9
Example result:
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



### GET: loinc/parts/<code>
Returns a json object with the description of this part code.  Attributes are as described in the multi-axial table.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/LP97384-9
Example result:
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



### GET: loinc/parts/parents/<code>
Returns a json list of the parents of the LOINC part code. The list contain one json for each parent.  Attributes are as described in the multi-axial table.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/parents/LP97384-9
Example result:
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



### GET: loinc/parts/descendants/<code>
Returns a json object listing the hierarchy below the search code.  The search code is the key to list of its children.  Each child is listed with a list of its children recusively.  Codes a listed with <code type>: code, name, e.g. LOINC part code: LP97384-9, HLA-DP+DQ+DR | Bld-Ser-Plas.
Example usage: https://loinc-part-search-demo.herokuapp.com/loinc/parts/descendants/LP56928-2
Example result:
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


