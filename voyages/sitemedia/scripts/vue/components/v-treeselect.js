// v-treeselect
Vue.component("v-treeselect", {
  props: ['title', 'description', 'varName', 'filter', "isImputed", "isAdvanced"],
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
      <div class="col-md-12">
        <treeselect
          :multiple="true"
          :options="options"
          placeholder="Select from the list"
          
          v-model="value"
        />
      </div>
    </div>

    <div class="row v-padding">
      <div class="col-md-12">
        <code>{{value}}</code>
      </div>
    </div>

    <div class="row v-padding">
      <div class="col-md-12">
        <b-button :disabled="!options.changed" variant="success" size="sm" @click="apply">Apply</b-button>
        <b-button :disabled="!options.changed" variant="secondary" size="sm" @click="reset">Reset</b-button>
      </div>
    </div>
  </div>

  `,

  components: {
    treeselect: window.VueTreeselect.Treeselect,
  },

  data: function(){
    return {
        value: null,
        options: [ {
          id: 'fruits',
          label: 'Fruits',
          children: [ {
            id: 'apple',
            label: 'Apple 🍎',
          }, {
            id: 'grapes',
            label: 'Grapes 🍇',
          }, {
            id: 'pear',
            label: 'Pear 🍐',
          }, {
            id: 'strawberry',
            label: 'Strawberry 🍓',
          }, {
            id: 'watermelon',
            label: 'Watermelon 🍉',
          } ],
        }, {
          id: 'vegetables',
          label: 'Vegetables',
          children: [ {
            id: 'corn',
            label: 'Corn 🌽',
          }, {
            id: 'carrot',
            label: 'Carrot 🥕',
          }, {
            id: 'eggplant',
            label: 'Eggplant 🍆',
          }, {
            id: 'tomato',
            label: 'Tomato 🍅',
          } ],
        } ],
    }
  },

  methods: {
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
});
// v-treeselect
