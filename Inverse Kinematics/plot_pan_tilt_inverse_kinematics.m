function plot_pan_tilt_inverse_kinematics(Px, Py, Pz)
    L1 = 0.11;
    L2 = 0.1;

    % Inverse kinematics
    theta1 = atan2(Py, Px);
    theta2 = acos((Pz - L1) / L2);

    % Forward kinematics
    x = L2 * cos(theta1) * sin(theta2);
    y = L2 * sin(theta1) * sin(theta2);
    z = L1 + L2 * cos(theta2);

    % Link positions
    link1_x = [0, 0];
    link1_y = [0, 0];
    link1_z = [0, L1];

    link2_x = [0, x];
    link2_y = [0, y];
    link2_z = [L1, z];

    % Plot the links and end effector position
    figure;
    plot3([link1_x; link2_x], [link1_y; link2_y], [link1_z; link2_z], 'LineWidth', 2);
    hold on;
    plot3(x, y, z, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    title('Pan-Tilt Mechanism');
    grid on;
    legend('Link 1', 'Link 2', 'End Effector');
    hold off;
end