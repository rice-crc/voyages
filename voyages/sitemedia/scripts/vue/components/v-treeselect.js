// v-treeselect
Vue.component("v-treeselect", {
  template: `
    <vue-treeselect
      :multiple="true"
      :options="options"
      placeholder="Select your favourite(s)..."
      v-model="value"
    />
    `,

  data: function(){
    return {
        value: null,
        options: ["node-1", "node-2"],
        source: [
          {
            id: 'node-1',
            label: 'Node 1',
            children: [
              {
                id: 'node-1-a',
                label: 'Node 1-A',
              },
            ],
          },
          {
            id: 'node-2',
            label: 'Node 2',
          },
        ],
      }
  }
});
// v-treeselect
