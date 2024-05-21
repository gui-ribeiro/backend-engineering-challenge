# Backend Engineering Challenge


## Setup the code

The code on this solution does not need any instalation in particular, just go ahead and clone this repo to your local pc and it's pretty much ready to use. If you want to run tests I recommend that you run the following command:

```
pip install -r requirements.txt
```

## Files explanation
There are 2 main folders, src and tests

### SRC

Inside this folder is the code to solve this challenge. It is properly commented. 

### TESTS

Inside this folder there is 1 python file and 3 JSON files. The python file has the only test developed for this code. It is a system test, and tests the correctness of the solution as a whole. The JSON files are used/produced in this test. Later in this document there is a more detailed explanation on these files.



## Run the code

To run the code you will need a input JSON file. After that just execute the following command:

```
cd src
python3 main.py --input_file input.json --window_size 10
```

This will produce a output.json file in the current directory with the results of the computation.

## Test the code

In order to test the code you can just run the following command (don't forget the setup step):

```
pytest tests/
```

This will take the input.json file as input and produce an output.json file on this same directory. It will then compare the output.json file with the expected_output.json file. To run this test for different test cases just change the input.json and expected_output.json files as you wish.

#### Notes

This section is a bit of an explanation to the solution.

The objective was to have a functional but efficient solution, not only on time but also on memory. To achieve this I chose to extract the most information possible when reading the input file, but also in a compact way, where no unecessary information is stored. For that I chose to store the sum of the duration of the translations and the number of translations for every minute, taking advantage of the ordered input. This way, not only there is no unnecessary information stored, but there is also no repeated computation for the average values. This information is stored in a dictionary as it has very low read time cost.

Another detail that will also save us some time is that nothing is ever out of order, therefore for the input there is no need to order anything, just write to a file, as it is already ordered.

There was also some attention to edge cases (division by zero, timestamps to be outputed), hopefully they are all covered :)
