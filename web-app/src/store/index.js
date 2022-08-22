import { createStore } from "vuex";
import { auth } from "./modules/auth";
import { faq } from "./modules/faq";
import { compatibility } from "./modules/compatibility";
import { json_schema_viewer } from "./modules/json_schema_viewer";

export default createStore({
  modules: {
    auth,
    faq,
    compatibility,
    json_schema_viewer,
  },
});
