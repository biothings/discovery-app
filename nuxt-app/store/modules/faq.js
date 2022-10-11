import diagram from "~~/assets/img/diagram.png";
import schemagraph from "~~/assets/img/schemagraph.png";
import dashhelp from "~~/assets/img/dashhelp.png";
import editor from "~~/assets/img/editor.png";
import guides from "~~/assets/img/guides.png";
import metadata from "~~/assets/img/metadata.png";
import metahelp from "~~/assets/img/metahelp.png";
import deletehelp from "~~/assets/img/deletehelp.png";
import privacy from "~~/assets/img/privacy.png";
import editmeta from "~~/assets/img/editmeta.png";

export const faq = {
  state: () => ({
    faqs: {
      dde: [
        {
          sectionName: "General",
          questions: [
            {
              anchor: "what-is-dde",
              question: "What is the Data Discovery Engine?",
              image: diagram,
              answer: `<p>
                                The Data Discovery Engine is a website that provides guidance for researchers on how to make their data discoverable and reusable, and bring the practical benefits of data sharing to researcher’s own research projects, as well as the research community as a whole.
                            </p>
                            <p class="alert alert-secondary">
                                <small>
                                Through it's three main components the Data Discovery Engine can support: the extension and reusability of schemas, structured metadata tools that utilize those schemas and making the resulting metadata accessible through our API and Data Portals supported. 
                                </small>
                                </p>`,
            },
            {
              anchor: "what-is-schema",
              question: "What is a schema?",
              image: schemagraph,
              answer: `<p>
                                Schemas can be thought of as a set of 'types', each associated with a set of properties that further define that type. The types are arranged in a hierarchy and each type inherits the properties of all its parents.
                                </p>
                                <p class="alert alert-info">
                                An example of a type's hierarchy can be seen here: <a href='https://schema.org/Thing' target="_blank">Thing</a> > <a href='https://schema.org/Person' target="_blank">Person</a> > <a href='https://schema.org/Patient' target="_blank">Patient</a>
                                </p>
                                <p>
                                We use <a href="https://schema.org/" target="_blank">Schema.org</a>'s schemas as the base vocabulary due to it's very generic nature. From that collection of schemas you can easily find a starting point, extend that schema and define more specific schemas related to your reserach.
                                </p>
                                <p>
                                All registered schemas are also available via our <a href="/registry">registry</a>. Feel free to browse it for existing examples.
                                </p>`,
            },
            {
              anchor: "data-portals",
              question: "What data portals are integrated into this project?",
              answer: `<p>
                                The Data Discovery Engine is built with a very extensible infrastructure based on reusability and thus it can easily integrate multi-purpose portals. 
                                </p>
                                <p>
                                The core of this project is based on <a href="https://schema.org/" target="_blank">Schema.org</a> and re-using and extending an existing microdata markup format to boost the discoverabilty of and findability of 
                                biomedical research. 
                                </p>
                                <p>
                                Currently it provides support for biomedical and COVID-19 focused portals.
                                </p>`,
            },
            {
              anchor: "add-portal",
              question:
                "Can we request to add our portal to the Discovery Data Engine?",
              answer: `<p>
                                If your data portal currently uses structured metadata or you believe it could benefit from ingesting structured metadata. You can use the tools we provide to author/covert your own schema and create custom validation rules.
                                </p>
                                <p>
                                With a customized schema and validation you can generate a dynamically generated form custom to your specifications and use it to format data to your schema structure.
                                </p>
                                <p>
                                If you believe the Discovery Data Engine could benefit from the addition of your portal based on the area of focus please <a href="https://github.com/biothings/discovery-app/issues/new">contact us</a>.
                                </p>`,
            },
            {
              anchor: "dashboard",
              question: "How do I access my dashboard?",
              image: dashhelp,
              answer: `<p>
                                Your user <a href="/dashboard">dashboard</a> is place where you can easily manage and quickly access your registered schemas and registered metadata. To view your dashboard you must log in using a valid <a href='https://github.com/' target="_blank">GitHub</a> account then click on your user image on the menu.
                                </p>
                                <p class="alert alert-info text-center">
                                <small>Options include: view, quick edit, make private/public, and delete.</small>
                                </p>`,
            },
            {
              anchor: "issue-report",
              question: "How can I report an issue or make a suggestion?",
              answer: `<p>
                                If you believe you have a great idea for a new feature or if you found an issue while using any of our tools please <a href="https://github.com/biothings/discovery-app/issues/new">create an issue</a> via GitHub and let us know what happened and how we can reproduce the issue.
                                </p>`,
            },
          ],
        },
        {
          sectionName: "Schema_Playground",
          questions: [
            {
              anchor: "what-is-schema-playground",
              question: "What is the Schema Playground?",
              answer: `<p>
                                The <a href="/schema-playground">Schema Playground</a> is a place where you can find a large number of existing bio-medical and general purpose schemas.
                                It is also a place where you can extend an existing schema to create your own, visualize and register* it to share with the community.
                                <ul>
                                    <li>
                                    <i class="text-danger">If you DON'T have a schema</i> > Search for existing schemas to re-use or extend an existing one.
                                    </li>
                                    <li>
                                    <i class="text-success">If you DO have a schema</i> > Visualize your schema and register it so others can re-use it and in turn helping our efforts to make data re-usable.
                                    </li>
                                </ul>
                                </p>
                                <p class="alert alert-secondary">
                                <small>
                                <i class="fas fa-asterisk"></i> You will need a valid <a href='https://github.com/' target="_blank">GitHub</a> account or an approved organization account to register new schemas. Sign up for one, it's easy and free!
                                </small>
                                </p>`,
            },
            {
              anchor: "choosing-schema",
              question: "How do I choose a schema to author my own?",
              answer: `<p>
                                Our <a href="/schema-playground">Schema Playground</a> features <b>common starting points</b> (Dataset, Protocols, etc) and also a <a href="/registry">registry</a> of classes from reputable sources to help you decide the right starting point.
                                </p>
                                <p>
                                You can browse existing schemas from the community and <a href="https://schema.org/" target="_blank">Schema.org</a> schemas in our <a href="/registry">registry</a>.
                                </p>`,
            },
            {
              anchor: "reuse-schema",
              question:
                "I found a schema that is perfect for me, how do I re-use it?",
              answer: `<p>
                                If you do not need to extend a schema and would like to use it as is, you can download it by clicking the <b>source</b> link in that schema's home page.
                                </p>
                                <p>
                                For example, here is the homepage of an extended Dataset schema you may want to re-use: <a target="_blank" href="/view/outbreak">https://discovery.biothings.io/view/outbreak</a>.
                                </p>`,
            },
            {
              anchor: "how-to-use-editor",
              question: "How do I use the schema editor?",
              image: editor,
              answer: `
                            <p>
                            Once you find a Class you wish to extend, you will be asked to choose a unique namespace that hasn't been registered before.  This will be the prefix attached to each new definition you provide.
                            Since you are extending a Class, you will be asked to create a new Class that is more specific to your needs but follows the same hierarchy as its parent Class.  Once that is done, you can begin picking
                            the properties from its parents that you want to use to define your metadata and finally add any new properties (8) not included with a proper unique name. 
                            </p>
                            <p>
                            Once you are happy with your schema definition you have an option to download (5) your work or if you logged in with GitHub, you may choose to use the built-in
                            GitHub tool to save your work directly to an existing or new public repository. Your saved work can then be visualized and registered via our Schema Playground, and you can easily manage your contributions 
                            via your own user dashboard.
                            </p>
                            <ol class="text-left">
                                <li>
                                Log-in status.
                                </li>
                                <li>
                                Preview your work.
                                </li>
                                <li>
                                Download your work.
                                </li>
                                <li>
                                Save to GitHub directly* Requires GitHub login and permission.
                                </li>
                                <li>
                                Add a new property to your class.
                                </li>
                                <li>
                                The extended Class you created.
                                </li>
                                <li>
                                Parent properties available to choose from.
                                </li>
                                <li>
                                Show/Hide all properties of this class.
                                </li>
                            </ol>`,
            },
            {
              anchor: "register-namespace",
              question:
                "What is a namespace and how do I register a custom namespace for my schema?",
              answer: `<p>
                                During the process of extending an existing schema via the <a href="/schema-playground">Schema Playground</a>
                                you are asked to choose a short name for new Class/property definitions. This name is also used to suggest the namespace registered with us when you visualize then register your schema.
                                The namespace will be the new homepage for your schema. E.g. <span class="text-info">http://discovery.biothings.io/view/<b>&lt;namespace&gt;</b></span>.
                                </p>
                                <p class="alert alert-secondary">
                                <small>Your namespace must be unique and it can only contain lower-case web-safe characters.</small>
                                </p>`,
            },
            {
              anchor: "schema-registration",
              question: "How do I register my schema?",
              answer: `<p>
                                After you log in the registration option will be available to you when you view your schema using it's url in the <a href="/schema-playground">Schema Playground</a>. Registration is simple and it only requires you to choose a <a href="#namespace">namespace</a>
                                </p>
                                <p class="alert alert-secondary">
                                <small>
                                <i class="fas fa-asterisk"></i> You will need a valid <a href='https://github.com/' target="_blank">GitHub</a> account or an approved organization account to register new schemas. Sign up for one, it's easy and free!
                                </small>
                                </p>`,
            },
            {
              anchor: "why-register",
              question: "Why should I register my schema?",
              answer: `<ul class="text-muted text-left">
                                <li>
                                    <i class="fas fa-check"></i> Share your work with other members of the community. Your schema definition could be helpful to many others in the community as a starting point for their reserach.
                                </li>
                                <li>
                                    <i class="fas fa-check"></i> By registering a schema derived from an existing schema you are helping to maintain the <a href="https://www.go-fair.org/fair-principles/" target="_blank">FAIR</a> (Findable, Accessible, Interoperable, Reusable) principles by making data more <b>Reusable</b>.
                                </li>
                                <li>
                                    <i class="fas fa-check"></i> It's easy to register your schema! If everything looks good here all you have to do is choose a namespace for your schema's homepage.
                                </li>
                                <li>
                                    <i class="fas fa-check"></i> You'll be able to easily share your schema and visualize it in a way that it's easy to understand.
                                </li>
                                </ul>`,
            },
          ],
        },
        {
          sectionName: "Discovery Guide",
          questions: [
            {
              anchor: "what-is-a-guide",
              question: "What is a guide?",
              image: guides,
              answer: `<p>
                                Guides allow you to contribute metadata to particular Data Portal. The generated metadata will be structured to that Data Portal's schema meaning that your metadata will be able to be integrated into that Data Portal.
                                </p>
                                <p>
                                Each Data Portal provides a guide based on a schema and that guide is dynamically generated based on that particular schema's validation rules to ensure that your input is valid and your contribution is ready to be integrated into that Portal.
                                </p>
                                `,
            },
            {
              anchor: "how-to-use-guide",
              question: "How do I use the discovery guide?",
              image: metadata,
              answer: `<p class="text-center">
                                <p>
                                    Select the portal you wish to contribute based on your interests and click on it's Add Dataset Metadata button. You will be taken to a form that will guide you through required and recommended fields by that portal.
                                </p>
                                <p>
                                    It's really easy and fast! Here's a quick introduction to the layout:
                                </p>
                                    <ol class="text-left">
                                    <li>
                                        (Login Status, Start Over, Preview Progress, Import Metadata, Bulk Registration, Issue Details)
                                    </li>
                                    <li>
                                        Current category.
                                    </li>
                                    <li>
                                        Change display settings.
                                    </li>
                                    <li>
                                        Clear/Complete (if viewing one item at a time) option.
                                    </li>
                                    <li>
                                        Track progress across categories.
                                    </li>
                                    <li>
                                        Issue details for that field.
                                    </li>
                                    <li>
                                        Continue to next page. (Available when requirements are met)
                                    </li>
                                    </ol>
                            </p>`,
            },
            {
              anchor: "access-contributions",
              question: "How do I access my contributions?",
              image: metahelp,
              answer: `<p>
                                After successfully contributing an item whether it is a schema or metadata you will be able to manage it via your <a href="/dashboard">dashboard</a>. To view your dashboard you must log in using a valid <a href='https://github.com/' target="_blank">GitHub</a> account or approved organization.
                                </p>
                                <p>
                                You can manage your registered schemas and metadata on your dashboard and each provides their own set of options. Take a look below: 
                                </p>
                                <p class="alert alert-info text-center">
                                <small>From your dashboard you can view, update and delete any registered item.</small>
                                </p>
                                <p class="alert alert-info text-center">
                                <small>Options include: view, quick edit, make private/public, and delete.</small>
                                </p>`,
            },
            {
              anchor: "delete-item",
              question: "How do I delete a registered schema or dataset?",
              image: deletehelp,
              answer: `<p>
                                Your user <a href="/dashboard">dashboard</a> is the place to do that. If you are the user that registered that item you will see it listed in your dashboard.
                                </p>
                                <p class="alert alert-danger text-center">
                                <small>Click on the <i class="fas fa-trash"></i> icon and it will be deleted. Warning: This action cannot be reverted!</small>
                                </p>`,
            },
            {
              anchor: "edit-privacy",
              question: "How do I make my dataset private/public?",
              image: privacy,
              answer: `<p>
                                All new entries are set to <b>PUBLIC</b> as default. You can change this anytime in your <a href="/dashboard">dashboard</a>.  Note: Making any changes to the metadata will revert its status to PUBLIC but you can change the setting once your are done.
                                </p>
                                <p class="alert alert-info text-center">
                                <small>Simply click on the <b>Edit Privacy</b> button and confirm the new status.</small>
                                </p>`,
            },
            {
              anchor: "edit-metadata",
              question: "How do I edit registered metadata?",
              image: editmeta,
              answer: `<p>
                                Each metadata entry is generated via a guide, so to properly edit an already registered item you will need to load it back into it's guide.
                                </p>
                                <p>
                                Choose the guide you previously used and choose <b>Import Metadata</b> from the guide menu and choose the item you want to edit. All available matching fields will be populated with your data. Note: If you change the <b>identifier</b> field it will result in creating a new registry item.
                                </p>
                                <p class="text-danger">
                                Note: Making any changes to the data will revert its privacy status to PUBLIC but you can change the setting once your are done in your dashboard.
                                </p>
                                <p class="alert alert-info text-center">
                                <small>Click on the <b>Load Existing Data</b> edit existing data.</small>
                                </p>`,
            },
          ],
        },
      ],
      n3c: [
        {
          sectionName: "VIRAL_VARIANCE",
          questions: [
            {
              anchor: "technical-specs",
              question: "Are they technical specifications available?",
              answer: `<p>
                            Yes, detailed technical specifications can be found <a href="https://github.com/National-COVID-Cohort-Collaborative/variants/wiki" target="_blank" rel="nonreferrer">here</a>.
                            </p>`,
            },
            {
              anchor: "contact-help",
              question: "Who do I contact for help?",
              answer: `<p>
                                    If you have questions about the please submit a ticket to:
                                </p>
                                <p>
                                    <ul>
                                        <li><a href="https://n3c-help.atlassian.net/servicedesk/customer/portal/2" target="_blank" rel="nonreferrer">N3C Enclave </a></li>
                                        <li><a href="mailto:n3csupport@datavant.com" target="_blank" rel="nonreferrer">Datavant PPRL (DV) <i class="fas fa-envelope"></i></a></li>
                                        <li><a href="https://submit.ncbi.nlm.nih.gov/" target="_blank" rel="nonreferrer">NCBI </a></li>
                                    </ul>
                                </p>`,
            },
            {
              anchor: "summary-and-data",
              question: "Do I need to send both the summary and sequence data?",
              answer: `<p>
                                    No, you do not.  The pandemic is a public health crisis, and we appreciate any information you are willing to send.  N3C has taken a phased approach to participation in viral variant information. 
                                </p>
                                <p>
                                    <b>Phase I</b> requires a simple file, CSV with 4 fields (Specimen ID, N3C pseudo-ID, Specimen Date and Viral Variant Summary) that you place in your existing organization’s N3C sFTP folder. 
                                </p>
                                <p>
                                    <table class="table">
                                        <thead>
                                            <tr>
                                            <th scope="col">Value Submitted</th>
                                            <th scope="col">Pango Sub_Lineage</th>
                                            <th scope="col">Pango Lineage</th>
                                            <th scope="col">WHO Lineage</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <th>"DELTA"</th>
                                                <td>NULL</td>
                                                <td>NULL</td>
                                                <td>DELTA</td>
                                            </tr>
                                            <tr>
                                                <th>"B.1.617.2"</th>
                                                <td>NULL</td>
                                                <td>B.1.617.2</td>
                                                <td>DELTA (imputed)</td>
                                            </tr>
                                            <tr>
                                                <th>"AY.4"</th>
                                                <td>AY.4</td>
                                                <td>B.1.617.2 (imputed)</td>
                                                <td>DELTA (imputed)</td>
                                            </tr>
                                            <tr>
                                                <th>DELTA, B.1.617.2</th>
                                                <td>NULL</td>
                                                <td>B.1.617.2 (parsed from text)</td>
                                                <td>DELTA (parsed from text)</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </p>
                                <p>
                                    <b>Phase II</b>  is the submission of the PPRL file to the honest broker and the submission of the viral variant sequence to NCBI. <a href="https://github.com/National-COVID-Cohort-Collaborative/variants/wiki" target="_blank" rel="nonreferrer">More info</a>.
                                </p>`,
            },
            {
              anchor: "access-to-data",
              question:
                "How can I get access to the linked viral variant sequence data and N3C medical history?",
              answer: `<p>
                                    Access to the integrated N3C data and NCBI viral variant sequence data will require an “Interconnect Agreement” between two or more NIH data enclaves at different institutes. The NIH Interconnect agreement is currently being developed but no timeframe for its availability has been established. 
                                </p>`,
            },
            {
              anchor: "info-variants",
              question: "Do you want information on every Viral Variants?",
              answer: `<p>
                                    We are initially only curating a subset  Variants Being Monitored (VBM) which can be found <a href="https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-classifications.html#anchor_1632158885160" target="_blank" rel="nonreferrer">here</a>.
                                </p>`,
            },
            {
              anchor: "who-pango-lineage",
              question: "What is WHO Lineage and PANGO Lineage?",
              answer: `<p>
                                    The World Health Organization, (WHO) Lineage is the “common name” and is always a Greek letter. This was implemented by the WHO to facilitate communications about viral variants (See below). 
                                </p>
                                <p>
                                    The WHO Linage is a very high-level concept or summary label of a viral variant. 
                                    Other lineages like <a href="https://cov-lineages.org/lineage_list.html target="_blank">PANGO</a> are ontologies and have thousands of rows that delineate anything from subtype of a viral variant to the earliest date recorded. 
                                    In addition, the WHO classification the CDC Classification can be found <a target="_blank" href="https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-classifications.html">here</a>.
                                </p>
                                <h3>World Health Organization, WHO - Naming SARS-CoV-2 variants <a href="https://www.who.int/news/item/31-05-2021-who-announces-simple-easy-to-say-labels-for-sars-cov-2-variants-of-interest-and-concern" target="_blank" rel="nonreferrer"><small>More info </small></a></h3>
                                <p>
                                    <blockquote>
                                        “The established nomenclature systems for naming and tracking SARS-CoV-2 genetic lineages by GISAID, Nextstrain and Pango are currently and will remain in use by scientists and in scientific research. 
                                        To assist with public discussions of variants, WHO convened a group of scientists from the WHO Virus Evolution Working Group (now called the Technical Advisory Group on Virus Evolution), 
                                        the WHO COVID-19 reference laboratory network, representatives from GISAID, Nextstrain, Pango and additional experts in virological, microbial nomenclature and communication from several countries and agencies to consider easy-to-pronounce and non-stigmatizing labels for VOI and VOC. 
                                        At the present time, this expert group convened by WHO has recommended using letters of the Greek Alphabet, i.e., Alpha, Beta, Gamma, Delta which will be easier and more practical to be discussed by non-scientific audiences” 
                                        .
                                    </blockquote>
                                </p>
                                <h3>Naming SARS-CoV-2 variants <a href="https://www.who.int/en/activities/tracking-SARS-CoV-2-variants/" target="_blank" rel="nonreferrer"><small>More info </small></a></h3>`,
            },
            {
              anchor: "parsing-info",
              question: "Do I need to parse the Viral Variant Summary data?",
              answer: `<p>
                                    <b>NO!</b> We want to make this is as easy as possible and will take any combination of WHO Lineage, or PANGO Parent or subtype values.  As long as the files include delimiters between values, N3C will parse and curate this information prior to it being made available for investigators in N3C.
                                </p>`,
            },
            {
              anchor: "for-investigators",
              question: "What information will be available for investigators?",
              answer: `<p>
                                    <table class="table">
                                        <thead>
                                            <tr>
                                            <th scope="col">Name</th>
                                            <th scope="col">Description</th>
                                            <th scope="col">Data Example</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <th>specimen_who_lineage</th>
                                                <td>
                                                    WHO Lineage Name this is a Greek Letter i.e., Alpha, Beta, Gamma, Delta which is easier and more practical to be discussed by non-scientific audiences 
                                                    <a href="https://www.who.int/en/activities/tracking-SARS-CoV-2-variants" target="_blank" rel="nonreferrer"><small>More info </small></a>
                                                </td>
                                                <td>Delta</td>
                                            </tr>
                                            <tr>
                                                <th>specimen_PANGO_lineage</th>
                                                <td>
                                                    “The PANGO nomenclature is being used by researchers and public health agencies worldwide to track the transmission and spread of SARS-CoV-2, including variants of concern. 
                                                    This website documents all current PANGO lineages and their spread, as well as various software tools which can be used by researchers to perform analyses on SARS-COV-2 sequence data” 
                                                    <a href="https://cov-lineages.org/index.html#about" target="_blank" rel="nonreferrer"><small>More info </small></a>                                                    <a href="https://www.who.int/en/activities/tracking-SARS-CoV-2-variants" target="_blank" rel="nonreferrer"><small>More info </small></a>
                                                </td>
                                                <td>B.1.617.2</td>
                                            </tr>
                                            <tr>
                                                <th>specimen_Pango Sub_Lineage</th>
                                                <td>
                                                    See above
                                                </td>
                                                <td>AY</td>
                                            </tr>
                                            <tr>
                                                <th>specimen_designation</th>
                                                <td>
                                                    Designation defines transmissibility, disease severity, risk of reinfection, and impacts on diagnostics and vaccine performance  
                                                    <a href="https://www.who.int/en/activities/tracking-SARS-CoV-2-variants" target="_blank" rel="nonreferrer"><small>More info </small></a>
                                                </td>
                                                <td>VOC</td>
                                            </tr>
                                            <tr>
                                                <th>specimen_date</th>
                                                <td>
                                                    The date the specimen was collected (dd/mm/yyyy) 
                                                    <a href="https://www.who.int/en/activities/tracking-SARS-CoV-2-variants" target="_blank" rel="nonreferrer"><small>More info </small></a>
                                                </td>
                                                <td>07/13/21</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </p>`,
            },
          ],
        },
        {
          sectionName: "MORTALITY",
          questions: [
            {
              anchor: "cause-of-death",
              question: "Can I tell if the cause of death was COVID?",
              answer: `<p>
                        Supplemental PPRL Mortality data does not indicate cause of death. The harmonized OMOP CDM may provide a cause of death that indicates the cause of death was COVID. However, the Government, Private Obituary, and <a target="_blank" href="ObituaryData.com">ObituaryData.com</a> sources do not provide a cause of death.  
                            </p>`,
            },
            {
              anchor: "data-details",
              question:
                "Why is there a higher incidence of deaths reported on the first day of the month or the 15th day of the month?",
              answer: `<p>
                            The Government source does not know the exact date of death for all reported deaths. If they know only the month of death (e.g., November 2021), they will provide the date of death as the first day of that month (e.g., 11/1/2021). If they know only the year of death (e.g., 2021), they will provide the date of death as the first day of that year (e.g., 1/1/2021). 
                            </p>
                            <p>
                                Likewise, the Private Obituary source does not know the exact date for all reported deaths. If they know only the month of death (e.g., November 2021), they will provide the date of death as either the first day of that month or the middle of that month (e.g., 11/1/2021 or 11/15/2021). If they know only the year of death (e.g., 2021), they will provide the date of death as the first day of that year (e.g., 1/1/2021). 
                            </p>`,
            },
            {
              anchor: "educational-resources",
              question:
                "Are there any training or educational resources for this dataset?",
              answer: `<p>
                        Several resources are available within the Enclave to learn more about both PPRL and the Mortality dataset. 
                        The <a target="_blank" href="https://unite.nih.gov/multipass/automatic-login?collector_type=saml&realm=nih-adfs&redirect-uri=%2Fmultipass%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3Dworkspace%26redirect_uri%3Dhttps%253A%252F%252Funite.nih.gov%252Fworkspace%252Fredirect%26response_type%3Dcode%26state%3DeyJpZCI6IjJhZmI3MjdhLTJjYTEtNGJkZS1iMGIxLWVmMTU0MGM0ZGJlZiIsInJlcSI6Ii93b3Jrc3BhY2UvbW9kdWxlL3ZpZXcvbGF0ZXN0L3JpLndvcmtzaG9wLm1haW4ubW9kdWxlLmU3YjgzYThjLTU0NWUtNDlhYy04NzE0LWYzNGJmYTdmNzc2Nz92aWV3PWZvY3VzJklkPTIzIn0">N3C PPRL Module</a> 
                        contains introductory information on both PPRL and the Mortality dataset. 
                        There is also a <a target="_blank" href="https://unite.nih.gov/multipass/automatic-login?collector_type=saml&realm=nih-adfs&redirect-uri=%2Fmultipass%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3Dworkspace%26redirect_uri%3Dhttps%253A%252F%252Funite.nih.gov%252Fworkspace%252Fredirect%26response_type%3Dcode%26state%3DeyJpZCI6ImI4NzI0YWQ0LTlmOWYtNGEwMy04YWNiLTIwOTlmOTk3NTE3ZSIsInJlcSI6Ii93b3Jrc3BhY2Uvbm90ZXBhZC92aWV3L3JpLm5vdGVwYWQubWFpbi5ub3RlcGFkLmU0NWNkMjBlLTlkYTktNDRjNy1iMWQxLTc0N2U3YzU2MTAyZiJ9">N3C PPRL Mortality Data Guide</a>, 
                        which contains more specific information about the Mortality dataset, and how to use it.</p>`,
            },
          ],
        },
      ],
    },
  }),
  getters: {
    getFAQ: (state) => (name) => {
      return state.faqs?.[name] ? state.faqs?.[name] : state.faqs.dde;
    },
  },
};
