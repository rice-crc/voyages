// v-treeselect
Vue.component("v-treeselect", {
  template: `
    <div>
      <treeselect
        :multiple="true"
        :options="options"
        placeholder="Select from the list"
        v-model="value"
      />
      <pre class="result">{{ value }}</pre>
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
  }
});
// v-treeselect
