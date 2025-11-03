// story.jsonnet
// This file defines the structure, assertions, and process of the research paper
// "Phonosematic Computational Topologies" using OWL and SHACL semantics in JSON-LD format.
{
  "@context": {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "sh": "http://www.w3.org/ns/shacl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "fabio": "http://purl.org/spar/fabio/",
    "pso": "https://gftd.ai/ontology/paper-structure-ontology#",
    "gftd": "https://gftd.ai/instance/",

    "label": "rdfs:label",
    "comment": "rdfs:comment"
  },

  "@graph": [
    // Ontology Definition
    {
      "@id": "pso:",
      "@type": "owl:Ontology",
      "label": "Paper Structure Ontology",
      "comment": "An ontology to describe the structure, assertions, and process of a research paper."
    },

    // Class Definitions
    { "@id": "pso:Paper", "@type": "owl:Class", "rdfs:subClassOf": "fabio:ResearchPaper" },
    { "@id": "pso:Section", "@type": "owl:Class", "rdfs:subClassOf": "fabio:Expression" },
    { "@id": "pso:Assertion", "@type": "owl:Class" },
    { "@id": "pso:ComputationalModel", "@type": "owl:Class" },
    { "@id": "pso:Visualization", "@type": "owl:Class", "rdfs:subClassOf": "fabio:Figure" },

    // Property Definitions
    { "@id": "pso:hasSection", "@type": "owl:ObjectProperty", "rdfs:domain": "pso:Paper", "rdfs:range": "pso:Section" },
    { "@id": "pso:makesAssertion", "@type": "owl:ObjectProperty", "rdfs:range": "pso:Assertion" },
    { "@id": "pso:supportedBy", "@type": "owl:ObjectProperty", "rdfs:domain": "pso:Assertion" },
    { "@id": "pso:describesModel", "@type": "owl:ObjectProperty", "rdfs:range": "pso:ComputationalModel" },
    { "@id": "pso:visualizedBy", "@type": "owl:ObjectProperty", "rdfs:range": "pso:Visualization" },

    // SHACL Shape Definitions
    {
      "@id": "pso:PaperShape",
      "@type": "sh:NodeShape",
      "sh:targetClass": "pso:Paper",
      "sh:property": [
        { "sh:path": "dc:title", "sh:minCount": 1, "sh:maxCount": 1, "sh:datatype": "xsd:string" },
        { "sh:path": "pso:hasSection", "sh:minCount": 1, "sh:nodeKind": "sh:IRI" },
        { "sh:path": "pso:makesAssertion", "sh:minCount": 1, "sh:nodeKind": "sh:IRI" }
      ]
    },
    {
      "@id": "pso:SectionShape",
      "@type": "sh:NodeShape",
      "sh:targetClass": "pso:Section",
      "sh:property": [
        { "sh:path": "dc:title", "sh:minCount": 1, "sh:maxCount": 1, "sh:datatype": "xsd:string" }
      ]
    },

    // --- Paper Instance ---
    {
      "@id": "gftd:paper/phonosematic-topologies",
      "@type": "pso:Paper",
      "dc:title": "Phonosematic Computational Topologies: A Network-based Typology of Phonological Structures",
      "dcterms:creator": { "@id": "https://jun.gftd.ai" },
      "pso:makesAssertion": { "@id": "gftd:assertion/main" },
      "pso:hasSection": [
        { "@id": "gftd:paper/phonosematic-topologies/abstract" },
        { "@id": "gftd:paper/phonosematic-topologies/introduction" },
        { "@id": "gftd:paper/phonosematic-topologies/framework" },
        { "@id": "gftd:paper/phonosematic-topologies/typology" },
        { "@id": "gftd:paper/phonosematic-topologies/analysis" },
        { "@id": "gftd:paper/phonosematic-topologies/implications" },
        { "@id": "gftd:paper/phonosematic-topologies/discussion" },
        { "@id": "gftd:paper/phonosematic-topologies/conclusion" }
      ]
    },

    // --- Main Assertions ---
    {
      "@id": "gftd:assertion/main",
      "@type": "pso:Assertion",
      "label": "Main Assertion",
      "comment": "Natural language phonological structures can be modeled and typified as network topologies, revealing their underlying computational processes.",
      "pso:supportedBy": [
        { "@id": "gftd:assertion/typology" },
        { "@id": "gftd:assertion/computational-correspondence" }
      ]
    },
    {
      "@id": "gftd:assertion/typology",
      "@type": "pso:Assertion",
      "label": "Typological Assertion",
      "comment": "Languages can be classified into archetypes (Star, Cyclic, Tree, etc.) and hybrid topologies based on their phonological network structure."
    },
    {
      "@id": "gftd:assertion/computational-correspondence",
      "@type": "pso:Assertion",
      "label": "Computational Correspondence Assertion",
      "comment": "Each topological type corresponds to a specific class of computational models (e.g., FSMs, Tree Algorithms, Tensor Algebra)."
    },

    // --- Sections ---
    {
      "@id": "gftd:paper/phonosematic-topologies/introduction",
      "@type": "pso:Section",
      "dc:title": "1. Introduction",
      "pso:makesAssertion": { "@id": "gftd:assertion/main" }
    },
    {
      "@id": "gftd:paper/phonosematic-topologies/framework",
      "@type": "pso:Section",
      "dc:title": "2. Theoretical Framework",
      "pso:describesModel": { "@id": "gftd:model/vowel-phase-space" }
    },
    {
      "@id": "gftd:paper/phonosematic-topologies/analysis",
      "@type": "pso:Section",
      "dc:title": "4. Analysis of Hybrid Topologies in Natural Languages",
      "pso:supportedBy": { "@id": "gftd:assertion/typology" },
      "pso:visualizedBy": [
        { "@id": "gftd:viz/japanese" },
        { "@id": "gftd:viz/english" },
        { "@id": "gftd:viz/chinese" },
        { "@id": "gftd:viz/semitic" }
      ]
    },

    // --- Models & Visualizations ---
    {
      "@id": "gftd:model/vowel-phase-space",
      "@type": "pso:ComputationalModel",
      "label": "Vowel Phase Space and Consonant Operator Model",
      "comment": "Models vowels as a phase space and consonants as operators that induce state transitions."
    },
    {
      "@id": "gftd:viz/japanese",
      "@type": "pso:Visualization",
      "dc:title": "Japanese Ring Topology",
      "dcterms:source": "./language_visualizations/japanese_ring/japanese_ring_topology.png"
    },
    {
      "@id": "gftd:viz/english",
      "@type": "pso:Visualization",
      "dc:title": "English Tree Topology",
      "dcterms:source": "./language_visualizations/english_tree/english_tree_topology.png"
    },
    {
      "@id": "gftd:viz/chinese",
      "@type": "pso:Visualization",
      "dc:title": "Chinese Lattice Topology",
      "dcterms:source": "./language_visualizations/chinese_lattice/chinese_lattice_topology.png"
    },
    {
      "@id": "gftd:viz/semitic",
      "@type": "pso:Visualization",
      "dc:title": "Semitic Layered Topology",
      "dcterms:source": "./language_visualizations/semitic_layered/semitic_layered_topology.png"
    }
  ]
}
