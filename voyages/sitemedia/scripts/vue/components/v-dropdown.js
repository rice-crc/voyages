Vue.component("v-dropdown", {
  props: ['title', 'description', 'options', 'isMultiple', 'clearable', 'variable'],
  template: `
  <div class="">
    <div class="v-title" v-text="title"></div>
    <div class="v-description" v-text="description"></div>
    <treeselect
      v-model="data.value"
      :multiple="isMultiple"
      :clearable="clearable"
      :close-on-select="true"
      :options="data.options">

      <label class="vue-treeselect__label" slot="option-label" slot-scope="{ node }" >
        {{ isImputed(node.label) ? trimImputedLabel(node.label) : node.label }}
        <b-badge pill
          v-if="isImputed(node.label)"
          v-b-tooltip.hover title="Calculated by an algorithm and not based on historical record."
          variant="secondary"
          class="v-badge-imputed">
          IMP
        </b-badge>
      </label>

    </treeselect>
  </div>
  `,

  components: {
    treeselect: window.VueTreeselect.Treeselect,
  },

  data: function(){
    return {
      data: {
        value: null,
        options: this.options
      }
    }
  },

  // at created, load default values for those who have them
  created: function () {
    if (typeof(this.variable) != "undefined") {
      if (this.variable.value !== null) {
        this.data.value = this.variable.value;
      }
    }
  },

  methods: {
    isImputed(label) {
      if (label.slice(-1) == "*") {
        return true
      } else {
        return false;
      }
    },
    trimImputedLabel(label) {
      return label.slice(0, -1);
    }
  },

  watch: {
    // search object
    data: {
      handler: function(){
        this.$emit('changed', this.variable.variable, this.data.value);
      },
      deep: true,
    },
  },


});
