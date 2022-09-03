import { createApp } from "vue";

import App from "./App.vue";
// Vue Ecosystem
import router from "./router";
import store from "./store";
// Plugins
import VueGtag from "vue-gtag-next";
import VueSweetalert2 from "vue-sweetalert2";
// Global Components
import CopyBtn from "./components/CopyBtn.vue";
import ResourceFieldBox from "./components/ResourceFieldBox.vue";
import PropertyBox from "./components/PropertyBox.vue";
import AnyOf from "./components/AnyOf.vue";
import OneOf from "./components/OneOf.vue";

import "./assets/main.css";
import "./assets/css/styles.css";
import "tippy.js/dist/tippy.css";
import "tippy.js/themes/light.css";
import "sweetalert2/dist/sweetalert2.min.css";
import "tabulator-tables/dist/css/tabulator.min.css";

/* FontAwesome core */
import { library } from "@fortawesome/fontawesome-svg-core";

/* FontAwesome components */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

/* import specific icons */
import {
  faCircle,
  faEye,
  faCode,
  faSyncAlt,
  faTrash,
  faBolt,
  faLock,
  faLockOpen,
  faStepBackward,
  faStepForward,
  faChevronRight,
  faExternalLinkAlt,
  faEnvelope,
  faCogs,
  faListOl,
  faTasks,
  faLightbulb,
  faPlus,
  faClipboard,
  faChevronLeft,
  faCheck,
  faCodeBranch,
  faSearch,
  faArrowRight,
  faUser,
  faBuilding,
  faTimes,
  faUndo,
  faSpinner,
  faMinusSquare,
  faPlusSquare,
  faHome,
  faNotEqual,
  faListUl,
  faDotCircle,
  faFileDownload,
  faExclamationCircle,
  faRegistered,
  faRetweet,
  faAsterisk,
  faSquare,
  faCaretRight,
  faTimesCircle,
  faFileMedical,
  faUserCheck,
  faSignInAlt,
  faPenSquare,
  faQuestionCircle,
  faStar,
  faInfoCircle,
  faMinusCircle,
  faCheckCircle,
  faEllipsisH,
  faMinus,
} from "@fortawesome/free-solid-svg-icons";
import { faGithub, faGithubAlt } from "@fortawesome/free-brands-svg-icons";

/* add icons to the library */
library.add(
  faGithub,
  faCircle,
  faEye,
  faCode,
  faSyncAlt,
  faTrash,
  faBolt,
  faLock,
  faLockOpen,
  faStepBackward,
  faStepForward,
  faChevronRight,
  faExternalLinkAlt,
  faEnvelope,
  faCogs,
  faListOl,
  faListUl,
  faTasks,
  faLightbulb,
  faPlus,
  faClipboard,
  faChevronLeft,
  faCheck,
  faCodeBranch,
  faSearch,
  faArrowRight,
  faUser,
  faBuilding,
  faTimes,
  faUndo,
  faSpinner,
  faMinusSquare,
  faPlusSquare,
  faHome,
  faNotEqual,
  faDotCircle,
  faFileDownload,
  faExclamationCircle,
  faRegistered,
  faRetweet,
  faAsterisk,
  faSquare,
  faCaretRight,
  faTimesCircle,
  faGithubAlt,
  faFileMedical,
  faUserCheck,
  faSignInAlt,
  faPenSquare,
  faQuestionCircle,
  faStar,
  faInfoCircle,
  faTimesCircle,
  faMinusCircle,
  faCheckCircle,
  faEllipsisH,
  faMinus,
  faTimesCircle

);

const app = createApp(App);

app
  .use(router)
  .use(VueGtag, {
    property: {
      id: "G-JDB8QD7ZPZ",
    },
  })
  .use(VueSweetalert2)
  .use(store);

app
  .component("CopyBtn", CopyBtn)
  .component("font-awesome-icon", FontAwesomeIcon)
  .component("ResourceFieldBox", ResourceFieldBox)
  // circular dependency components need to be global
  .component("PropertyBox", PropertyBox)
  .component("AnyOf", AnyOf)
  .component("OneOf", OneOf);

// dev base api url
app.config.globalProperties.$apiUrl =
  !process.env.NODE_ENV == "development"
    ? "http://localhost:8000"
    : "https://discovery.biothings.io";

app.mount("#app");
