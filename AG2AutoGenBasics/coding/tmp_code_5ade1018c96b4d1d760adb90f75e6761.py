import matplotlib.pyplot as plt
import numpy as np

def plot_sine_wave():
    # Generate x values from -2π to 2π
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

    # Calculate corresponding y values (sine of x)
    y = np.sin(x)

    # Create the plot
    plt.plot(x, y)

    # Set title and labels
    plt.title('Sine Wave')
    plt.xlabel('x')
    plt.ylabel('sin(x)')

    # Save the plot to a file
    plt.savefig('sine_wave.png')

    # Show the plot (optional)
    # plt.show()

if __name__ == "__main__":
    plot_sine_wave()