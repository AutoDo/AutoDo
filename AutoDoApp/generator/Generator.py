# This python module is for document generator module


from AutoDoApp.generator.GeneratorCommunicator import GeneratorCommunicator
import pydotplus




class Generator(GeneratorCommunicator):

    def generate_document(self):
        raise NotImplementedError("You must implement this methods!")

    def send_complete_notification(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_readme_md(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_api(self):
        raise NotImplementedError("You must implement this methods!")

    def generate_graph(self,data):

        '''data = [("class A","class B","method A to B"),
               ("class B","class C","method B to C"),
                ("class C","class A","method C to A"),
                ("class C", "class A", "method C' to A'"),
                ("class C", "class A", "method C'' to A''"),
                ("class A","class A","method A to A"),
                ("class B","class B","method B to B"),
                ("class C","class C","method C to C")]
        '''
        graph = pydotplus.Dot(graph_type="digraph")

        # let's add the relationship between the king and vassals
        for i in range(len(data)):
            edge = pydotplus.Edge(data[i][0], data[i][1], label=data[i][2])
            graph.add_edge(edge)


        # ok, we are set, let's save our graph into a file
        graph.write_png('example1_graph.png')

        #raise NotImplementedError("You must implement this methods!")


if __name__ == "__main__":
    gen = Generator()
    data = [('Math(object)', 'Circle', 'get_areaget_area()'), ('Math(object)', 'Circle', 'get_circumferenceget_circumference()'), ('Math(object)', 'Triangle', 'check_anglecheck_angle()'), ('Math(object)', 'Square', 'get_areaget_area()'), ('Math(object)', 'Square', 'get_heightget_height()'), ('Math(object)', 'Square', 'get_widthget_width()')]
    gen.generate_graph(data)