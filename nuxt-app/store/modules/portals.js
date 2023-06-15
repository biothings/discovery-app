import cd2h from "~~/assets/img/cd2h-logo-white.png";
import dde from "~~/assets/img/dde-logo-o.svg";
import n3c from "~~/assets/img/N3Co.png";
import n3cLogo from "~~/assets/img/N3Cwhite.png";
import outbreak from "~~/assets/img/outbreak_white.svg";
import niaidIcon from "~~/assets/img/niaid/icon.svg";
import outbreakIcon from "~~/assets/img/icon-01.svg";

export const portals = {
  state: () => ({
    portals: [
      {
        name: "Outbreak.info",
        shortName: "Outbreak.info",
        keyName: "outbreak",
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
        coverage: ["Dataset"],
        guides: [
          {
            guide: "/guide/outbreak/dataset",
            name: "Dataset",
            registry: "/dataset?template=/guide/outbreak/dataset",
          },
        ],
        datasets: "/dataset?template=/guide/outbreak/dataset",
        colors: [{ hex: "#D13B62" }, { hex: "#0A253D" }],
      },
      {
        name: "NIAID Systems Biology",
        shortName: "NIAID SysBio",
        keyName: "niaid",
        header:
          "The NIAID Systems Biology Consortium for Infectious Diseases Data Dissemination Working Group works to make our research outputs more FAIR.",
        linkname: "niaid",
        description: `<p>
          The NIAID (National Institute of Allergy and Infectious Diseases) Systems Biology Consortium for Infectious Diseases Data Dissemination Working Group works to make our research outputs more FAIR.
          </p><p>
          We developed a Dataset and ComputationalTool schema tailored for research outputs in the infectious disease research space to increase their findability and discoverability.
          </p>
          <p>
          To help researchers easily collect and publish these metadata, the DDE registry allows researchers to easily collect dataset metadata based on our standards when no community repository exists.
          </p>`,
        image: niaidIcon,
        portalicon: niaidIcon,
        site: "",
        schema: "/view/niaid",
        coverage: ["Dataset", "ComputationalTool"],
        guides: [
          {
            guide: "/guide/niaid",
            name: "Dataset",
            registry: "/dataset?template=niaid:dataset",
          },
          {
            guide: "/guide/niaid/ComputationalTool",
            name: "Computational Tool",
            registry: "/dataset?template=niaid:computationaltool",
          },
        ],
        datasets: "/dataset?template=niaid:dataset",
        colors: [{ hex: "#369AC1" }, { hex: "#113B56" }],
        publications: [
          {
            name: "Developing a standardized but extendable framework to increase the findability of infectious disease datasets",
            link: "https://www.biorxiv.org/content/10.1101/2022.10.10.511492v1",
          },
        ],
      },
      {
        name: "CTSA National Center for Data to Health",
        shortName: "CD2H",
        keyName: "cd2h",
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
        coverage: ["Dataset"],
        guides: [
          {
            guide: "/guide",
            name: "Dataset",
            registry: "/dataset?template=/guide",
          },
        ],
        api: "https://crawler.biothings.io/",
        datasets: "/dataset?template=/guide",
        colors: [{ hex: "#63296B" }, { hex: "#4A7D8F" }],
      },
      {
        name: "The National COVID Cohort Collaborative (N3C)",
        shortName: "N3C",
        keyName: "n3c",
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
        coverage: ["Dataset"],
        guides: [
          {
            guide: "/guide/n3c/dataset",
            name: "Dataset",
            registry: "/dataset?template=/guide/n3c/dataset",
          },
        ],
        datasets: "/dataset?template=/guide/n3c/dataset",
        colors: [{ hex: "#4B7E8F" }, { hex: "#64296B" }],
        faq_link: "/faq/n3c",
      },
    ],
  }),
  getters: {
    getPortals: (state) => {
      return state.portals;
    },
  },
};