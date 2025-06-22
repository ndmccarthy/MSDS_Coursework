SELECT productLine, SUM(quantityOrdered * priceEach) AS productLineProfit
        FROM products P
			JOIN orderdetails D ON P.productCode = D.productCode
            JOIN orders O ON D.orderNumber = O.orderNumber
		WHERE year(orderDate) = 2004
        GROUP BY productLine
        ORDER BY 2 DESC LIMIT 3;

SELECT officeCode, ROUND(SUM(quantityOrdered * priceEach)/COUNT(employeeNumber), 2) AS averageEmployeeSales
	FROM employees E 
		JOIN customers C ON E.employeeNumber = C.salesRepEmployeeNumber
		JOIN orders O ON C.customerNumber = O.customerNumber
		JOIN orderdetails D ON D.orderNumber = O.orderNumber
    GROUP BY officeCode
    ORDER BY 2 DESC LIMIT 1;

SELECT CONCAT(firstName, ' ', lastName) AS employee
	FROM customers C 
		JOIN employees E ON C.salesRepEmployeeNumber = E.employeeNumber
        LEFT JOIN orders O ON O.customerNumber = C.customerNumber
        WHERE O.ordernumber IS NULL;
    