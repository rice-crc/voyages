// input (select + textbox x 2)
Vue.component('v-input', {
  props: ['title', 'description', 'varName', 'searchTermCaption', 'filter', "isNumeric", "isImputed", "isAdvanced"],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{title}}</span>
        <span>
          <b-badge
            v-if="isImputed"
            v-b-tooltip.hover title="Imputed variables are calculated by an algorithm and not based on historical records."
            variant="warning"
            class="v-badge-imputed">
            Imputed
          </b-badge>
          <b-badge
            v-if="isAdvanced"
            v-b-tooltip.hover title="Advanced variables are additional parameters that are frequenlty used. They do not change current search behavior."
            variant="danger" class="v-badge-advanced">Advanced</b-badge>
        </span>
      </div>
      <div class="v-description" v-text="description"></div>

      <div class="row">
        <div class="col-md-12" v-if="!isNumeric">
          <v-textbox @blurred="updateSearchTerm0" :search-term-caption="options.searchTermCaption0" :value="item.searchTerm0"></v-textbox>
        </div>
        <div class="col-md-4" v-if="isNumeric">
          <v-select @changed="updateOp" :value="item.op" :isNumeric="isNumeric"></v-select>
        </div>
        <div class="col-md-4" v-if="isNumeric && options.searchTerm1Disabled">
          <v-textbox @blurred="updateSearchTerm0" :search-term-caption="options.searchTermCaption0" :value="item.searchTerm0" :type="options.type"></v-textbox>
        </div>
        <div class="col-md-8" v-if="isNumeric && !options.searchTerm1Disabled">
          <v-textbox @blurred="updateSearchTerm0" :search-term-caption="options.searchTermCaption0" :value="item.searchTerm0" :type="options.type"></v-textbox>
        </div>
        <div class="col-md-4" v-if="options.searchTerm1Disabled && isNumeric ">
          <v-textbox @blurred="updateSearchTerm1" :search-term-caption="options.searchTermCaption1" :value="item.searchTerm1" :type="options.type"></v-textbox>
        </div>
      </div>

      <!--<div class="row v-padding">
        <div class="col-md-12">
          <code>{{item}}</code>
        </div>
      </div>-->

      <!--
      <div class="row v-padding">
        <div class="col-md-12">
          <b-button variant="success" size="sm" @click="apply">Apply</b-button>
          <b-button variant="secondary" size="sm" @click="reset">Reset</b-button>
        </div>
      </div>
      -->
    </div>
  `,

  data: function() {
    return {
      item: {
        varName: this.varName,
        searchTerm0: this.filter.current.searchTerm[0],
        searchTerm1: this.filter.current.searchTerm[1],
        op: "equals to",
      },
      options: {
        searchTerm1Disabled: false,
        searchTermCaption0: null,
        searchTermCaption1: null,
        type: "text",
      }
    }
  },

  methods: {
    // form element handlers
    updateSearchTerm0(value) { // handler for variable
      this.item.searchTerm0 = value;
    },
    updateSearchTerm1(value) { // handler for variable
      this.item.searchTerm1 = value;
    },
    updateOp(value) { // handler for variable
      this.item.op = value;
    },

    // form action buttons
    apply() { // simply return the search string to whichever requested for it
      var searchString = JSON.stringify(this.item);
      alert(searchString);
    },
    reset() { // reset data; observers will take care of resetting the controls
      this.item.searchTerm0 = null;
      this.item.searchTerm1 = null;
      this.item.op = "equals to";
    }
  },

  watch: {
    // search object
    item: {
      handler: function(){
        this.$emit('updated', this.item);

        // form specific logic
        if (this.item.op == "between") {
          this.options.searchTerm1Disabled = true;
          this.options.searchTermCaption0 = "Enter the lower bound";
          this.options.searchTermCaption1 = "Enter the upper bound";
        } else {
          this.options.searchTerm1Disabled = false;
          this.item.searchTerm1 = null;
          if (this.item.op == "is less than") {
            this.options.searchTermCaption0 = "Enter the upper bound";
          }
          if (this.item.op == "is more than") {
            this.options.searchTermCaption0 = "Enter the lower bound";
          }
          if (this.item.op == "equals to") {
            this.options.searchTermCaption0 = this.searchTermCaption;
          }
        }
      },
      deep: true,
    },
  },

  mounted: function() {
    this.options.searchTermCaption0 = this.searchTermCaption;
    this.options.type = this.isNumeric ? "number" : "text";
  }

})
// end of input
