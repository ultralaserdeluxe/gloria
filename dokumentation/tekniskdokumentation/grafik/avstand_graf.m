% Jämför uppmätta värden med den använda funktionen

Y_left = [110, 96, 83, 73, 64, 57, 52, 47, 44, 40, 36, 34, 32, 30, 28, 27, 25, 24, 24, 22, 21, 20, 20, 19, 18, 17];
Y_right = [102, 89, 77, 68, 61, 54, 49, 45, 42, 39, 36, 34, 32, 30, 28, 26, 25, 24, 24, 22, 22, 21, 21, 20, 20, 20];


Y_both = [Y_left,Y_right];
X_range = [(4:1:29),(4:1:29)];

%X = linspace(4,29);
%Z = (X-49.0)/31.0;
%Y = (0.14*(power(Z,6)))-(0.96*(power(Z,5)))+(2.4*(power(Z,4)))-(3.2*(power(Z,3)))+(4.4*(power(Z,2)))-(8.3*Z) + 13

xlabel('Uppmätt Y');
ylabel('X');
plot(X_range, Y_both, '+');
grid on;