import cd2h from  "~~/assets/img/cd2h-logo-white.png"
import dde from  "~~/assets/img/dde-logo-o.svg"
import n3c from  "~~/assets/img/N3Co.png"
import n3cLogo from  "~~/assets/img/N3Cwhite.png"
import outbreak from  "~~/assets/img/outbreak_white.svg"
import niaid from  "~~/assets/img/niaid/logo.svg"
import niaidIcon from  "~~/assets/img/niaid/icon.svg"
import outbreakIcon from  "~~/assets/img/icon-01.svg"


export const portals = {
  state: () => ({
    portals: [
        {
          name: "Outbreak.info",
          header:
            "During outbreaks of emerging diseases such as COVID-19, efficiently collecting, sharing, and integrating data is critical to scientific research. Outbreak.info is a resource to aggregate all this information into a single location.",
          linkname: "outbreak",
          description: `<p>
            In response to the current outbreak of SARS-CoV-2 (the virus that causes COVID-19), researchers worldwide have been generating and openly sharing data, publications, reagents, code, protocols, and more. Broad sharing of these research resources improves the speed and efficiency of science. Unfortunately, there are no uniform standards and repositories for collecting all this information in one place.
            </p><p>
            Outbreak.info focuses on aggregating all SARS-CoV-2 / COVID-19 information into a single site. We focus on making the metadata about these resources more standardized, on creating web interfaces to make the resources more findable, and on a few focused data integration efforts to make data more usable.
            </p>`,
          image: outbreak,
          portalicon: outbreakIcon,
          api: "https://api.outbreak.info/",
          site: "https://outbreak.info/",
          schema: "/view/outbreak",
          guides: [
            {
              guide: "/guide/outbreak/dataset",
              name: "Dataset",
              registry: "/dataset?guide=/guide/outbreak/dataset",
            },
          ],
          datasets: "/dataset?guide=/guide/outbreak/dataset",
          colors: [{ hex: "#D13B62" }, { hex: "#0A253D" }],
        },
        {
          name: "NIAID Data Portal",
          header:
            "AN AGGREGATOR OF OPEN DATASETS, WITH A PARTICULAR FOCUS ON ALLERGY AND INFECTIOUS DISEASES",
          linkname: "niaid",
          description: `<p>
            The NIAID (National Institute of Allergy and Infectious Diseases) Data Portal aggregates <b class="tip text-info" data-tippy-content="Omics DI,NCBI GEO, Zenodo, Harvard Dataverse, NYU Data Catalog, ImmPort, Data Discovery Engine">7 different data sources</b> together in a searchable platform, making it easier to find datasets.
            </p><p>
            We also standardize the dataset metadata to a common form, increasing the findability of these datasets. Schema.org provides a widely accepted format regonizable by major search engines and data portals.
            </p><p>
            While some dataset providers already use this format to describe their datasets, others provide structured metadata in their own format. Learn more about our efforts to encapsulate non-standard dataset metdata in schema.org's format.
            </p>`,
          image: niaid,
          portalicon: niaidIcon,
          site: "https://discovery.biothings.io/niaid/",
          schema: "/view/niaid",
          guides: [
            {
              guide: "/guide/niaid",
              name: "Dataset",
              registry: "/dataset?guide=/guide/niaid",
            },
            {
              guide: "/guide/niaid/ComputationalTool",
              name: "Computational Tool",
              registry: "/dataset?guide=/guide/niaid/ComputationalTool",
            },
          ],
          datasets: "/dataset?guide=/guide/niaid",
          colors: [{ hex: "#369AC1" }, { hex: "#113B56" }],
        },
        {
          name: "CTSA National Center for Data to Health",
          header:
            "A CD2H PROJECT TO PROMOTE FAIR DATA-SHARING BEST PRACTICES & MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS",
          linkname: "cd2h",
          description: `<p>
              Informatics advancements, coupled with a shift towards open science, are in the process of fundamentally transforming how we approach translational research and clinical care. The CTSA Program is poised to help realize precision medicine by leveraging informatics tools and expertise within CTSA hubs to solve key informatics challenges across the translational spectrum.
            </p><p>
            The CD2H was funded in fall 2017 to coordinate and integrate informatics for the CTSA Program by promoting data reuse and interoperability, tool sharing, informatics fluency, and collaboration. We are here to serve the CTSA Program by creating additional resources, building impactful infrastructure, and further coalescing the community to develop and implement innovative solutions.
            </p><p>
            Towards these goals, CD2H seeks input from, and collaboration with, the CTSA Program. We convene the community through our CORES and Community Projects focused on data, software, and people; and partner with the community to iteratively develop solutions through CD2H Labs and our DREAM Challenges. The ultimate goal of the CD2H is to help CTSA Hubs thrive, accelerate advancements in informatics, and improve patient care.
            </p>`,
          image: cd2h,
          portalicon: dde,
          site: "https://ctsa.ncats.nih.gov/cd2h/",
          schema: "/view/biomedical",
          guides: [
            {
              guide: "/guide",
              name: "Dataset",
              registry: "/dataset?guide=/guide",
            },
          ],
          api: "https://crawler.biothings.io/",
          datasets: "/dataset?guide=/guide",
          colors: [{ hex: "#63296B" }, { hex: "#4A7D8F" }],
        },
        {
          name: "The National COVID Cohort Collaborative (N3C)",
          header:
            "The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.",
          linkname: "n3c",
          description: `<p>
              The National COVID Cohort Collaborative (N3C) is a complementary and synergistic partnership among the <a href="https://ncats.nih.gov/ctsa" target="_blank">Clinical and Translational Science Awards (CTSA) Program</a> hubs, the <a href="https://cd2h.org/" target="_blank">National Center for Data to Health (CD2H)</a>, distributed clinical data networks (PCORnet, OHDSI, ACT/i2b2, TriNetX), and other partner organizations, with overall stewardship by NIH’s  <a href="https://ncats.nih.gov/" target="_blank">National Center for Advancing Translational Sciences (NCATS)</a>.
            </p><p>
              The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.
            </p>`,
          image: n3cLogo,
          portalicon: n3c,
          site: "https://covid.cd2h.org/N3C",
          schema: "/view/n3c",
          guides: [
            {
              guide: "/guide/n3c/dataset",
              name: "Dataset",
              registry: "/dataset?guide=/guide/n3c/dataset",
            },
          ],
          datasets: "/dataset?guide=/guide/n3c/dataset",
          colors: [{ hex: "#4B7E8F" }, { hex: "#64296B" }],
          faq_link: "/faq/n3c",
        },
      ]
  }),
  getters: {
    getPortals: (state) => {
      return state.portals;
    },
  },
};
