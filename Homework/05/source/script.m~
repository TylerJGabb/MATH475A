clc;
clear all;
close all;    
M = csvread('duck.csv');
x_vec = M(:,1);
f_vec = M(:,2)



%Create the matrix X

for m = [20]
    for i = 1:numel(x_vec)
        j = 1;
        for pow = 0:m
            X(:,j) = x_vec.^pow;
            j = j + 1;
        end
    end

%-------- Solving the system--------------

    X
    X_t = X';

    A = X_t * X;
    b = X_t * f_vec;
    
    
    
    %solve Aa = b
    a = fliplr((A\b)')
 %-------------------------------------------
 
    test = linspace(0,14,100);
    f_c = polyval(a,test);
    scatter(x_vec,f_vec,'ro','MarkerFaceColor', 'r');
    ylim([0,3]);
    hold on
    plot(test,f_c,'k-','linewidth',2);
    print(sprintf('matlab_lsq_%d',m),'-dpng');
    abs(100*(f_vec - polyval(a,x_vec))./f_vec)
    close all;
    
 %------Compare with Lagrangian-----------------
    
 
    
    
 
end


