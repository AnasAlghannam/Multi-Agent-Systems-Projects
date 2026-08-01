import matplotlib.pyplot as plt
import numpy as np

# Generate x values from -2π to 2π
x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

# Calculate corresponding y values (sine of x)
y = np.sin(x)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Sine Wave')

# Add title and labels
plt.title('Sine Wave from -2π to 2π')
plt.xlabel('x')
plt.ylabel('sin(x)')

# Add legend
plt.legend()

# Save the plot as sine_wave.png
plt.savefig('sine_wave.png')

# Display the plot
plt.show()