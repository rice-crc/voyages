template = `
  <div class="v-form-group">
    <div class="v-title">
      <span>{{filter.label}}</span>
      <b-badge pill
        v-if="filter.options.isImputed"
        v-b-tooltip.hover title="` +
  gettext('Imputed results are calculated by an algorithm.') +
        `" variant="secondary"
        class="v-badge-imputed">` +
  gettext('IMPUTED') +
      `</b-badge>
      <!--
      <b-badge
        v-if="filter.options.isAdvanced"
        v-b-tooltip.hover title="{% trans 'Advanced variables are additional parameters that are frequenlty used. They do not change current search behavior.' %}"
        variant="danger" class="v-badge-advanced">Advanced</b-badge>
      -->
    </div>
    <div class="v-description" v-text="filter.description"></div>

    <div class="row">
      <div class="col-md-12">
        <treeselect
          :load-options="loadOptions"
          :multiple="true"
          :loading="true"
          :options=treeselectOptions
          :auto-load-root-options=isAutoLoaded
          :default-expand-level="1"
          :placeholder=filter.options.caption
          v-model="item.searchTerm"
        />
      </div>
    </div>

    <div class="row v-padding" v-if="false">
      <div class="col-md-12">
        <div>
          <code>{{item}}</code>
        </div>
        <div>
          <b-button :disabled="!options.changed" variant="success" size="sm" @click="apply">` +
          gettext('Apply') +
          `</b-button>
          <b-button :disabled="!options.changed" variant="secondary" size="sm" @click="reset">` +
          gettext('Reset') +
          `</b-button>
        </div>
      </div>
    </div>
  </div>
  `;

// v-treeselect
Vue.component("v-treeselect", {
  props: ['filter'],
  template: template,
  components: {
    treeselect: window.VueTreeselect.Treeselect,
  },

  data: function(){
    return {
      item: {
        varName: this.filter.varName,
        searchTerm: this.filter.default.searchTerm,
        op: this.filter.default.op,
      },
      options: {
        caption: this.filter.options.caption,
        changed: false,
      },
      treeselectOptions: null,
      isAutoLoaded: true,
    }
  },

  methods: {
    // form action buttons
    apply() { // simply return the search string to whichever requested for it
      var searchString = JSON.stringify(this.item);
      alert(searchString);
    },

    reset() { // reset data; observers will take care of resetting the controls
      this.item.searchTerm = null;
    },

    // load options for the v-treeselect componenet
    loadOptions({callback}) {
      // four parameters
      // this.$root - main Vue.js instance
      // this - this v-treeselect component
      // filter - filter object
      // callback - comes from the vue-treeselect plugin
      loadTreeselectOptions(this.$root, this, this.filter, callback);
    },
  },

  watch: {
    // search object
    item: {
      handler: function(){
        // control visibility
        if (this.item.searchTerm !== null && this.item.searchTerm.length > 0) {
          this.options.changed = true;
          this.$emit('change', this.item, true);
        } else {
          this.options.changed = false;
          this.$emit('change', this.item, false);
        }
      },
      deep: true,
    },

    // update prop 'filter' from store
    filter: {
      handler: function(value){
        // fill filter values to UI element
        this.item.searchTerm = this.filter.value.searchTerm;
      },
      deep: true,
    }
  },


});
// v-treeselect
