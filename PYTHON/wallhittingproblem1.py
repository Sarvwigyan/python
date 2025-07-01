import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, CheckButtons
import sys

# Constants
G = 9.81  # m/s^2
COEFFICIENT_OF_RESTITUTION = 0.7
DRAG_COEFFICIENT = 0.47
AIR_DENSITY = 1.225  # kg/m^3
BALL_RADIUS = 0.1  # m
BALL_MASS = 0.5  # kg

class ProjectileSimulation:
    def __init__(self):
        # Check if running in Jupyter
        self.is_jupyter = 'ipykernel' in sys.modules
        if self.is_jupyter:
            print("Running in Jupyter: Ensure '%matplotlib notebook' or '%matplotlib widget' is set.")

        # Set up figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        plt.subplots_adjust(bottom=0.35, left=0.25)
        
        # Default parameters
        self.theta = np.radians(37)
        self.u = 50
        self.wall_distance = 80
        self.wall_height = 40
        self.air_resistance = 0.0
        self.wind_speed = 0.0
        self.is_running = False
        self.is_paused = False
        
        # Initialize plot elements
        self.ball, = self.ax.plot([], [], 'ro', markersize=10, label='Projectile')
        self.trajectory, = self.ax.plot([], [], 'b-', alpha=0.3, linewidth=1.5, label='Trajectory')
        self.wall = self.ax.axvline(self.wall_distance, color='k', linestyle='-', linewidth=3, label='Wall')
        self.wall_patch = self.ax.fill_between([self.wall_distance-0.5, self.wall_distance+0.5], 
                                             0, self.wall_height, color='gray', hatch='//', alpha=0.5)
        self.wall_top = self.ax.axhline(self.wall_height, color='k', linewidth=3)
        self.ground = self.ax.axhline(0, color='saddlebrown', linewidth=2, label='Ground')
        self.ax.legend(loc='upper right')
        self.ax.set_facecolor('#e6f3ff')
        self.fig.patch.set_facecolor('#f0f0f0')
        
        # Setup controls
        self.setup_controls()
        
        # Initial trajectory
        self.x_vals, self.y_vals, self.total_time = self.calculate_trajectory()
        self.update_plot()
        
    def setup_controls(self):
        axcolor = 'lightgoldenrodyellow'
        ax_theta = plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor)
        ax_u = plt.axes([0.15, 0.20, 0.7, 0.03], facecolor=axcolor)
        ax_dist = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
        ax_height = plt.axes([0.15, 0.10, 0.7, 0.03], facecolor=axcolor)
        ax_air = plt.axes([0.15, 0.05, 0.7, 0.03], facecolor=axcolor)
        ax_wind = plt.axes([0.15, 0.00, 0.7, 0.03], facecolor=axcolor)
        
        self.s_theta = Slider(ax_theta, 'Angle (deg)', 0.1, 89.9, valinit=37)
        self.s_u = Slider(ax_u, 'Velocity (m/s)', 1, 100, valinit=50)
        self.s_dist = Slider(ax_dist, 'Wall Distance (m)', 10, 200, valinit=80)
        self.s_height = Slider(ax_height, 'Wall Height (m)', 5, 100, valinit=40)
        self.s_air = Slider(ax_air, 'Air Resistance', 0, 1, valinit=0)
        self.s_wind = Slider(ax_wind, 'Wind Speed (m/s)', -20, 20, valinit=0)
        
        self.s_theta.on_changed(self.update_params)
        self.s_u.on_changed(self.update_params)
        self.s_dist.on_changed(self.update_params)
        self.s_height.on_changed(self.update_params)
        self.s_air.on_changed(self.update_params)
        self.s_wind.on_changed(self.update_params)
        
        resetax = plt.axes([0.05, 0.05, 0.1, 0.04])
        launchax = plt.axes([0.05, 0.10, 0.1, 0.04])
        pauseax = plt.axes([0.05, 0.15, 0.1, 0.04])
        trail_ax = plt.axes([0.05, 0.20, 0.1, 0.04])
        
        self.button_reset = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
        self.button_launch = Button(launchax, 'Launch', color=axcolor, hovercolor='0.975')
        self.button_pause = Button(pauseax, 'Pause/Resume', color=axcolor, hovercolor='0.975')
        self.trail_check = CheckButtons(trail_ax, ['Show Trail'], [True])
        self.show_trail = True
        
        self.button_reset.on_clicked(self.reset)
        self.button_launch.on_clicked(self.launch)
        self.button_pause.on_clicked(self.pause_resume)
        self.trail_check.on_clicked(self.toggle_trail)
        
    def update_params(self, val):
        self.theta = np.radians(self.s_theta.val)
        self.u = self.s_u.val
        self.wall_distance = self.s_dist.val
        self.wall_height = self.s_height.val
        self.air_resistance = self.s_air.val
        self.wind_speed = self.s_wind.val
        self.is_running = False
        self.is_paused = False
        self.x_vals, self.y_vals, self.total_time = self.calculate_trajectory()
        self.update_plot()
        
    def reset(self, event):
        self.s_theta.reset()
        self.s_u.reset()
        self.s_dist.reset()
        self.s_height.reset()
        self.s_air.reset()
        self.s_wind.reset()
        self.is_running = False
        self.is_paused = False
        self.x_vals, self.y_vals, self.total_time = self.calculate_trajectory()
        self.update_plot()
        
    def launch(self, event):
        self.is_running = True
        self.is_paused = False
        self.update_plot()
        
    def pause_resume(self, event):
        self.is_paused = not self.is_paused
        self.update_plot()
        
    def toggle_trail(self, label):
        self.show_trail = not self.show_trail
        self.update_plot()
        
    def calculate_trajectory(self):
        if self.u < 1e-6:
            return [0], [0], 0.1
        
        ux = self.u * np.cos(self.theta)
        uy = self.u * np.sin(self.theta)
        
        dt = 0.01
        t = 0
        x, y = 0, 0
        vx, vy = ux, uy
        x_vals = [x]
        y_vals = [y]
        area = np.pi * BALL_RADIUS**2
        k = 0.5 * self.air_resistance * DRAG_COEFFICIENT * AIR_DENSITY * area / BALL_MASS
        
        while y >= 0 or t == 0:
            v = np.sqrt((vx - self.wind_speed)**2 + vy**2)
            ax = -k * v * (vx - self.wind_speed)
            ay = -G - k * v * vy
            
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt
            
            if self.wall_distance - BALL_RADIUS <= x <= self.wall_distance + BALL_RADIUS and 0 < y <= self.wall_height:
                vx = -vx * COEFFICIENT_OF_RESTITUTION
                vy *= COEFFICIENT_OF_RESTITUTION
                x = self.wall_distance
            
            if y < 0:
                y = 0
                vy = -vy * COEFFICIENT_OF_RESTITUTION
                vx *= COEFFICIENT_OF_RESTITUTION
            
            x_vals.append(x)
            y_vals.append(max(y, 0))
            t += dt
            
            if t > 20 or (abs(vx) < 0.1 and abs(vy) < 0.1 and y == 0):
                break
        
        return x_vals, y_vals, t
        
    def update_plot(self):
        if hasattr(self, 'anim'):
            self.anim.event_source.stop()
            del self.anim
        
        self.wall.set_xdata([self.wall_distance, self.wall_distance])
        self.wall_top.set_ydata([self.wall_height, self.wall_height])
        self.wall_top.set_xdata([self.wall_distance - 1, self.wall_distance + 1])
        self.wall_patch.remove()
        self.wall_patch = self.ax.fill_between([self.wall_distance-0.5, self.wall_distance+0.5], 
                                             0, self.wall_height, color='gray', hatch='//', alpha=0.5)
        
        max_x = max(max(self.x_vals + [self.wall_distance + 20]), 100)
        max_y = max(max(self.y_vals + [self.wall_height + 20]), 50)
        self.ax.set_xlim(0, max_x)
        self.ax.set_ylim(0, max_y)
        self.ax.set_xlabel('Horizontal Distance (m)')
        self.ax.set_ylabel('Vertical Height (m)')
        self.ax.set_title('Realistic Projectile Simulation with Wall Bounce')
        self.ax.grid(True, alpha=0.3)
        
        if self.show_trail:
            self.trajectory.set_data(self.x_vals, self.y_vals)
        else:
            self.trajectory.set_data([], [])
        
        max_frames = 500
        if len(self.x_vals) > max_frames:
            step = len(self.x_vals) // max_frames
            frames = range(0, len(self.x_vals), step)
        else:
            frames = range(len(self.x_vals))
        
        def init():
            self.ball.set_data([], [])
            if self.show_trail:
                self.trajectory.set_data(self.x_vals, self.y_vals)
            else:
                self.trajectory.set_data([], [])
            return self.ball, self.trajectory
        
        def animate(i):
            if self.is_running and not self.is_paused and i < len(self.x_vals):
                # Simulate spin by varying marker size
                spin_size = 10 + 2 * np.sin(i * 0.1)
                self.ball.set_markersize(spin_size)
                self.ball.set_data([self.x_vals[i]], [self.y_vals[i]])
                if not self.show_trail:
                    idx = min(i + 1, len(self.x_vals))
                    self.trajectory.set_data(self.x_vals[:idx], self.y_vals[:idx])
            return self.ball, self.trajectory
        
        interval = 33  # ~30 FPS
        self.anim = animation.FuncAnimation(
            self.fig, animate, frames=frames,
            init_func=init, blit=True, interval=interval, repeat=True)
        
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

if __name__ == "__main__":
    try:
        plt.ion()
        sim = ProjectileSimulation()
        plt.show(block=True)
    except Exception as e:
        print(f"Error: {e}")