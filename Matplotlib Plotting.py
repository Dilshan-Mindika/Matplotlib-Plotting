import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PlottingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Plotting Application")
        self.root.configure(bg='#f0f0f0')  # Set background color

        # Apply some styling to ttk elements
        self.style = ttk.Style()
        self.style.configure('TButton',
                             font=('Helvetica', 12, 'bold'), 
                             background="black",  # Background remains black
                             foreground="black",  # Text color is black now
                             padding=10)
        self.style.map('TButton',
                       background=[('active', '#333333'), ('disabled', '#e0e0e0')])

        self.style.configure('TLabel', font=('Helvetica', 10), background="#f0f0f0")
        self.style.configure('TCombobox', font=('Helvetica', 10), background="#ffffff")
        self.style.configure('TEntry', font=('Helvetica', 10), background="#ffffff")

        # Store plot history as a list of dictionaries
        self.plot_history = []

        # Create a Frame for plot controls
        self.control_frame = ttk.LabelFrame(self.root, text="Plot Controls", padding="10", style="TFrame")
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Plot Type Selection
        self.plot_type_label = ttk.Label(self.control_frame, text="Select Plot Type:")
        self.plot_type_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.plot_type = ttk.Combobox(self.control_frame, values=["Line", "Scatter", "Bar", "Histogram", 
                                                                 "Pie", "Area", "Box", "Hexbin", "Stacked Bar"])
        self.plot_type.set("Line")
        self.plot_type.grid(row=0, column=1, padx=5, pady=5)
        
        # X-axis values input
        self.xlabel_label = ttk.Label(self.control_frame, text="Enter X Values (comma separated):")
        self.xlabel_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.xlabel_entry = ttk.Entry(self.control_frame)
        self.xlabel_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Y-axis values input
        self.ylabel_label = ttk.Label(self.control_frame, text="Enter Y Values (comma separated):")
        self.ylabel_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.ylabel_entry = ttk.Entry(self.control_frame)
        self.ylabel_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Add message for user guidance
        self.helper_label = ttk.Label(self.control_frame, text='* Use commas to separate values (e.g., "1,2,3,4")', style="TLabel")
        self.helper_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Color input
        self.color_label = ttk.Label(self.control_frame, text="Plot Color:")
        self.color_label.grid(row=4, column=0, padx=5, pady=5)
        
        self.color_entry = ttk.Entry(self.control_frame)
        self.color_entry.grid(row=4, column=1, padx=5, pady=5)

        # Grid line checkbox
        self.grid_var = tk.BooleanVar()
        self.grid_checkbox = ttk.Checkbutton(self.control_frame, text="Show Grid", variable=self.grid_var)
        self.grid_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Plot Button with black text color
        self.plot_button = ttk.Button(self.control_frame, text="Generate Plot", command=self.generate_plot)
        self.plot_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        # Add Clear Button with black text color
        self.clear_button = ttk.Button(self.control_frame, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # History Button to display past plots
        self.history_button = ttk.Button(self.control_frame, text="View Plot History", command=self.view_plot_history)
        self.history_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Save as PDF Button
        self.save_pdf_button = ttk.Button(self.control_frame, text="Save as PDF", command=self.save_as_pdf)
        self.save_pdf_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Create a Frame for displaying the plot
        self.plot_frame = ttk.Frame(self.root, padding="10")
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Display the initial empty plot
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack()

        # Footer with copyright and "Powered by DILA" link
        self.footer_frame = ttk.Frame(self.root, padding="10")
        self.footer_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.copyright_label = ttk.Label(self.footer_frame, text="© 2025 All rights reserved.", font=("Helvetica", 10), background="#f0f0f0")
        self.copyright_label.grid(row=0, column=0, padx=5, pady=5)

        # "Powered by" text
        self.powered_by_label = ttk.Label(self.footer_frame, text="Powered by ", font=("Helvetica", 10), background="#f0f0f0")
        self.powered_by_label.grid(row=0, column=1, padx=5, pady=5)

        # Hyperlink for "DILA" only
        self.dila_label = ttk.Label(self.footer_frame, text="DILA", font=("Helvetica", 10, 'underline'), foreground="blue", cursor="hand2")
        self.dila_label.grid(row=0, column=2, padx=5, pady=5)
        self.dila_label.bind("<Button-1>", self.open_dila_website)

    def open_dila_website(self, event):
        # Open the DILA website in the default web browser
        webbrowser.open("https://dilshan-mindika-portfolio.vercel.app/")

    def generate_plot(self):
        # Disable the button temporarily
        self.plot_button.config(state=tk.DISABLED)

        # Clear previous plot
        self.ax.clear()

        # Retrieve user inputs
        plot_type = self.plot_type.get()
        xlabel = self.xlabel_entry.get()
        ylabel = self.ylabel_entry.get()
        color = self.color_entry.get()
        grid = self.grid_var.get()

        # Check if color is valid, else default to blue
        if not color:
            color = 'blue'

        try:
            # Convert comma-separated values into lists of numbers
            x = np.array([float(i) for i in xlabel.split(',')])
            y = np.array([float(i) for i in ylabel.split(',')])

            # Ensure x and y have the same length
            if len(x) != len(y):
                messagebox.showerror("Error", "The number of X and Y values must be the same.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values separated by commas.")
            return

        # Choose plot type
        if plot_type == "Line":
            self.ax.plot(x, y, color=color)
        elif plot_type == "Scatter":
            self.ax.scatter(x, y, color=color)
        elif plot_type == "Bar":
            self.ax.bar(x, y, color=color)
        elif plot_type == "Histogram":
            self.ax.hist(y, bins=30, color=color)
        elif plot_type == "Pie":
            self.ax.pie(y, labels=x, autopct='%1.1f%%', startangle=90, colors=[color]*len(y))
        elif plot_type == "Area":
            self.ax.fill_between(x, y, color=color, alpha=0.6)
        elif plot_type == "Box":
            self.ax.boxplot([y], patch_artist=True, boxprops=dict(facecolor=color))
        elif plot_type == "Hexbin":
            self.ax.hexbin(x, y, gridsize=50, cmap='Blues')
            self.figure.colorbar(self.ax.collections[0], ax=self.ax, label='Counts')
        elif plot_type == "Stacked Bar":
            self.ax.bar(x, y, color=color, stacked=True)

        # Set plot title and labels
        self.ax.set_title("Plot Title")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Show grid if checked
        if grid:
            self.ax.grid(True)
        else:
            self.ax.grid(False)

        # Redraw the canvas with the new plot
        self.canvas.draw()

        # Store the plot in history
        plot_data = {
            'type': plot_type,
            'x': xlabel,
            'y': ylabel,
            'color': color,
            'grid': grid
        }
        self.plot_history.append(plot_data)

        # Re-enable the plot button
        self.plot_button.config(state=tk.NORMAL)

    def save_as_pdf(self):
        # Ask the user to select a location and filename to save the plot
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                # Save the current figure as a PDF
                self.figure.savefig(file_path, format="pdf")
                messagebox.showinfo("Save as PDF", f"Plot saved successfully as {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot as PDF: {e}")

    def view_plot_history(self):
        # Show a simple dialog with the history of plots
        if not self.plot_history:
            messagebox.showinfo("Plot History", "No plots have been generated yet.")
            return
        
        history_message = "Generated Plots:\n"
        for idx, plot in enumerate(self.plot_history):
            history_message += f"{idx+1}. Type: {plot['type']}, X: {plot['x']}, Y: {plot['y']}, Color: {plot['color']}, Grid: {plot['grid']}\n"
        
        messagebox.showinfo("Plot History", history_message)

    def clear_all(self):
        # Reset all entries and controls
        self.xlabel_entry.delete(0, tk.END)
        self.ylabel_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.plot_type.set("Line")
        self.grid_var.set(False)

        # Clear the plot
        self.ax.clear()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingApp(root)
    root.mainloop()
