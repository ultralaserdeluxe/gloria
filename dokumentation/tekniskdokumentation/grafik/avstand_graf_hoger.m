
Y_right = [102, 89, 77, 68, 61, 54, 49, 45, 42, 39, 36, 34, 32, 30, 28, 26, 25, 24, 24, 22, 22, 21, 21, 20, 20, 20];

X_range = (4:1:29);

X = linspace(4,29);
Z = (X-50.0)/31.0;
Y = (0.041*(power(Z,6)))-(0.38*(power(Z,5)))+(1.5*(power(Z,4)))-(3.3*(power(Z,3)))+(5.3*(power(Z,2)))-(8.3*Z) + 13

xlabel('Uppmätt Y');
ylabel('X');
plot(X, Y, X_range, Y_right, '+');
grid on;