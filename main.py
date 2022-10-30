from Shapes import Shapes

def main():
    while True:
        try:
            # d is the length of rectangle
            d = float(input("Input length of rectangle: "))
            # r is the width of rectangle
            r = float(input("Input width of rectangle: "))
            if d < 0 or r < 0:
                raise TypeError
            if d < r:
                raise Exception
            result = Shapes.calculate_the_area_of_a_rectangle(d, r)
            print("The area of a rectangle is: ", result)
            break
        except ValueError:
            print("Please input a number!\n")
        except TypeError:
            print("Please input a positive number!\n")
        except Exception:
            print("The length must bigger the width!!!!!!!!!!!!\n")


if __name__ == "__main__":
    main()