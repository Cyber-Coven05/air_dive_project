class Docstrings:
    def __init__(self, name : str, id_number : int, value : float):
        """
        This class is a test for docstrings, it prints a test function

        :param name: name parameter is for naming the object
        :param id_number: specific ID for the object
        :param value: value given to the obejct

        """
        name = self.name
        id_number = self.id_number
        value = self.value

    def myfunction(self):
         """
         function that returns text

        :return text: returns text varriable 
         
         """
         text = 'this is my function'
         return text



myDocstring = Docstrings()