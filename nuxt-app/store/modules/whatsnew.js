import newFeature from "~~/assets/img/new-feature-01.svg";
import fix from "~~/assets/img/fix-01.svg";

export const news = {
  state: () => ({
    news: {
      2022: {
        October: [
          {
            id: "221",
            title: "Schema Cardinality Added",
            description: `The schema class visualizations now include property cardinality.  Cardinality is not automatically imported as well when you choose to extend a class that includes cardinality.`,
            icon: newFeature,
            link: "/schema-playground",
          },
        ],
        May: [
          {
            id: "222",
            title: "Metadata Registry Downloads",
            description: `The DDE's metadata registry now allows single or bulk item download in addition to being able to download as JSON or CSV.`,
            icon: newFeature,
            link: "/resource",
          },
          {
            id: "223",
            title: "Automatic Schema Updates",
            description: `The DDE will periodically check all registered schemas and update on our database if new changes are found without any errors.`,
            icon: newFeature,
            link: "",
          },
        ],
      },
      2023: {
        April: [
          {
            id: "000a",
            title:
              "Schema Visualizer Improvement for Visualizing Marginality Settings",
            description: `The schema playground has been updated to better display and filter properties based on marginality. This new feature is sure to maximize your productivity when viewing and considering a particular schema for your purposes.`,
            icon: fix,
            link: "/schema-playground",
          },
          {
            id: "0000",
            title: "Schema Uptime Status Tracking",
            description: `A new feature has been added that tracks the uptime of a schema's URL. This is an important addition as it allows users to quickly identify any issues with the availability of their schema, ensuring that it is always accessible when needed. The feature works by periodically checking the schema's URL and providing users with information about its availability, including any downtime that may have occurred. This information can be used to identify and address any issues that may be impacting the availability of the schema, ensuring that it remains reliable and accessible at all times. Overall, this new feature is an important addition for anyone who works with schemas and wants to ensure that they are always available when needed.`,
            icon: newFeature,
            link: "/validator",
          },
          {
            id: "0001",
            title: "New Metadata Validator",
            description:
              "A new validation tool has been developed to validate metadata, which can be incredibly helpful for data professionals, researchers, and anyone else who needs to ensure the accuracy and completeness of their data. This tool allows users to upload their metadata files and run a validation check to identify any errors or inconsistencies that may exist. By using this tool, users can save time and effort by quickly identifying and correcting any issues with their metadata, which can help to improve the quality and reliability of their data. Overall, this new online tool is a valuable resource for anyone who works with data and wants to ensure that their metadata is accurate and reliable.",
            icon: newFeature,
            link: "/validator",
          },
          {
            id: "0002",
            title: "Metadata Coverage Available",
            description:
              "A new page has been created that shows metadata coverage for a particular dataset. This page provides users with valuable information about the completeness and accuracy of the metadata associated with a dataset. Users can easily see which fields are covered by the metadata and which are not, allowing them to identify any potential gaps in their metadata coverage. This information is especially important for researchers and data professionals who rely on accurate and complete metadata to ensure that their data is reliable and can be easily understood and used by others. With the help of this new page, users can quickly assess the quality of their metadata and make any necessary improvements to ensure that their data is of the highest possible quality. Overall, this new page is a valuable tool for anyone who works with data and wants to ensure that their metadata is accurate and complete.",
            icon: newFeature,
            link: "/coverage",
          },
          {
            id: "0003",
            title: "Schema Editor Rebuilt, Improved Tools and Layout",
            description: `Our popular schema editor has gone a major redesign to make sure you can take advantage of all the inherited features of a particular schema so you can focus more on implementing new changes and not worry about the inheritance issues. Within the editor all the editing tools have been improved and resized for ease of use and readability.`,
            icon: fix,
            link: "/editor",
          },
          {
            id: "0004",
            title: "Schema Playground Redesign",
            description: `The schema playground has been completely redesigned to help you get to the tools you need faster if you are an experienced user while giving cleaner look easier to understand for new users.`,
            icon: fix,
            link: "/schema-playground",
          },
          {
            id: "0005",
            title: "DDE Rebuilt using Nuxt & Vue3",
            description: `The popular data exploration site, Data Discovery Engine, is undergoing a major rebuild using Nuxt and Vue 3. This is great news for data enthusiasts and researchers alike as it promises to provide a better user experience and increased functionality. Nuxt is a powerful framework for building server-side rendered Vue.js applications, while Vue 3 offers significant performance improvements and new features such as the Composition API. With the use of these technologies, the Data Discovery Engine will be able to provide faster and more efficient data analysis, visualization, and exploration. The new site is expected to be launched soon, and it's sure to be a valuable resource for anyone looking to explore and analyze data.`,
            icon: fix,
            link: "",
          },
        ],
      },
    },
  }),
  getters: {
    getNews: (state) => {
      return state.news;
    },
  },
};
