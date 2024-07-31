import scripps_img from "@/assets/img/scripps-logo.png";

export const about = {
  state: () => ({
    teams: [
      {
        image: scripps_img,
        name: "Scripps Research",
        members: [
          {
            name: "Andrew",
            lastname: "Su",
            title: "Professor",
            work_logo: scripps_img,
            work_website: "https://www.scripps.edu/",
            bio: "",
            education: [],
            image: "https://sulab.org/images/Andrew_Su_smll.jpg",
            personal_site: "https://sulab.org/members/andrew-su.html",
            links: [
              { title: "twitter", href: "https://twitter.com/chunleiwu" },
              { title: "github", href: "https://github.com/newgene" },
              {
                title: "linkedin",
                href: "https://www.linkedin.com/in/chunleiwu",
              },
            ],
          },
          {
            name: "Chunlei",
            lastname: "Wu",
            title: "Professor",
            work_logo: scripps_img,
            work_website: "https://www.scripps.edu/",
            bio: "Chunlei Wu is a Professor in the Department of Integrative Structure and Computational Biology at Scripps Research. Prior to joining Scripps in July 2011, he was the Research Investigator II at the Genomics Institute of the Novartis Research Foundation (GNF) in San Diego, CA.  More details about Chunlei's lab are available at https://wulab.io.",
            education: [
              "Ph.D., Biomathmetics and biostatistics, The University of Texas Health Science Center at Houston",
            ],
            image:
              "http://www.gravatar.com/avatar/108605daee6b3c24d02db9753637a66b?s=200",
            personal_site: "https://wulab.io/the-team-chunlei-wu",
            links: [
              { title: "twitter", href: "https://twitter.com/chunleiwu" },
              { title: "github", href: "https://github.com/newgene" },
              {
                title: "linkedin",
                href: "https://www.linkedin.com/in/chunleiwu",
              },
            ],
          },
          {
            name: "Marco",
            lastname: "Cano",
            title: "Research Programmer III",
            work_logo: scripps_img,
            work_website: "https://www.scripps.edu/",
            bio: "I'm a full-stack web developer with a background in Web/Graphic Design and Multimedia Animation. Love to build professional modern websites using the latest technologies and the best possible UI/UX design. Currently working for the Su/Wu Lab at Scripps Research.  Current projects include: http://BioThings.io and http://SmartAPI.info",
            education: [
              "3D Animation and Multimedia Design -Palomar College",
              "Full Stack Web Development – UCSD",
            ],
            image:
              "https://avatars1.githubusercontent.com/u/23092057?s=460&v=4",
            personal_site: "https://wulab.io/the-team-marco-alvarado",
            links: [
              { title: "twitter", href: "" },
              { title: "github", href: "https://github.com/marcodarko" },
              {
                title: "linkedin",
                href: "https://www.linkedin.com/in/marco-alvarado-cano",
              },
            ],
          },
          {
            name: "Nichollette",
            lastname: "Acosta",
            title: "Research Programmer III",
            work_logo: scripps_img,
            work_website: "http://sulab.org/",
            bio: "I am joining as a research programmer in 2021. I enjoy machine learning, bioinformatics and building software tools. Prior to this, I coded, primarily with fMRI brain data, for a Neuropsychology Ingestive Behavior lab.",
            education: [
              "BSc. in Computer Science, Minor in Bioinformatics, UNC at Charlotte",
            ],
            image: "https://wulab.io/content/images/2021/09/nicholla.jpg",
            personal_site: "https://wulab.io/the-team-nichollette-acosta",
            links: [
              { title: "twitter", href: "" },
              { title: "github", href: "https://github.com/NikkiBytes" },
              {
                title: "linkedin",
                href: "https://www.linkedin.com/in/nichollette-acosta/",
              },
            ],
          },
          {
            name: "Everaldo Rodrigo",
            lastname: "Rodolpho",
            title: "Research Programmer III",
            work_logo: scripps_img,
            work_website: "http://sulab.org/",
            bio: "Digital Convergence of SCORM Learning Objects.",
            education: ["M.S. Computer Science"],
            image:
              "https://wulab.io/content/images/2022/12/everaldo_rodolpho.jpeg",
            personal_site:
              "https://wulab.io/the-team-everaldo-rodrigo-rodolpho",
            links: [
              { title: "twitter", href: "" },
              { title: "github", href: "" },
              { title: "linkedin", href: "" },
            ],
          },
          {
            name: "Ginger",
            lastname: "Tsueng",
            title: "Staff Scientist",
            work_logo: scripps_img,
            work_website: "http://sulab.org/",
            bio: "",
            education: [
              "M.S. OHSU, Bioinformatics and Computational Biomedicine",
              "B.A. Northwestern University, Biology and Chemistry",
            ],
            image: "https://sulab.org/images/gtpic.jpg",
            personal_site: "https://wulab.io/the-team-ginger-tsueng",
            links: [
              { title: "twitter", href: "" },
              { title: "github", href: "" },
              { title: "linkedin", href: "" },
            ],
          },
        ],
      },
    ],
    pastContributors: [
      {
        name: "Xinghua (Jerry)",
        lastname: "Zhou",
        github: "https://github.com/namespacestd0",
      },
      {
        name: "Jiwen (Kevin)",
        lastname: "Xin",
        github: "https://github.com/kevinxin90",
      },
      {
        name: "Laura",
        lastname: "Hughes",
        github: "https://github.com/flaneuse",
      },
    ],
  }),
  getters: {
    teams: (state) => {
      return state.teams;
    },
    pastContributors: (state) => {
      return state.pastContributors;
    },
  },
};
